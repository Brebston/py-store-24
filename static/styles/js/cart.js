const API_CART = "/cart/api/";
const API_ADD_ITEM = "/cart/api/items/";
const API_CLEAR = "/cart/api/clear/";


function showMessage(text, type = "success") {
  const container = document.getElementById("message-container");

  const message = document.createElement("div");
  message.className = `message ${type}`;
  message.innerText = text;

  container.appendChild(message);

  setTimeout(() => {
    message.remove();
  }, 3000);
}

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== "") {
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
      break;
    }
  }
}
return cookieValue;
}

const csrftoken = getCookie("csrftoken");

function formatMoney(value) {
const number = Number(value || 0);
return `$${number.toFixed(2)}`;
}

async function fetchCart() {
  const response = await fetch(API_CART);
  if (!response.ok) {
  throw new Error("Failed to load cart");
}
return await response.json();
}

async function updateItem(itemId, quantity) {
  const response = await fetch(`/cart/api/items/${itemId}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ quantity }),
  });

  let data;

  try {
    data = await response.json();
  } catch (e) {
    throw new Error("Server error (not JSON)");
  }

  if (!response.ok) {
    throw new Error(data.error || data.detail || "Error");
  }

  return data;
}

async function deleteItem(itemId) {
  const response = await fetch(`/cart/api/items/${itemId}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
  });

if (!response.ok) {
  throw new Error("Failed to delete item");
}
return await response.json();
}

async function clearCart() {
  const response = await fetch(API_CLEAR, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
});

if (!response.ok) {
  throw new Error("Failed to clear cart");
}
return await response.json();
}

function renderCart(cart) {
const tbody = document.getElementById("cart-table-body");
const badge = document.getElementById("cart-badge");
const itemsCount = document.getElementById("summary-items");
const subtotalEl = document.getElementById("summary-subtotal");
const shippingEl = document.getElementById("summary-shipping");
const taxEl = document.getElementById("summary-tax");
const totalEl = document.getElementById("summary-total");
const checkoutBtn = document.getElementById("checkout-btn");

badge.textContent = cart.total_items || 0;
itemsCount.textContent = cart.total_items || 0;

subtotalEl.textContent = formatMoney(cart.subtotal);
shippingEl.textContent = formatMoney(cart.shipping);
taxEl.textContent = formatMoney(cart.tax);
totalEl.textContent = formatMoney(cart.total);

if (!cart.items || cart.items.length === 0) {
  tbody.innerHTML = `
    <tr>
      <td colspan="4" class="empty-cart">Your cart is empty.</td>
    </tr>
  `;
  checkoutBtn.classList.add("checkout-disabled");
  return;
}

checkoutBtn.classList.remove("checkout-disabled");

tbody.innerHTML = cart.items.map(item => `
  <tr>
    <td>
      <div style="display:flex; gap:12px; align-items:center">
        <div>
          <b>${item.product.name}</b>
          <div class="muted" style="font-size:13px">Slug: ${item.product.slug}</div>
          <button class="remove-btn" type="button" onclick="handleRemove(${item.id})">Remove</button>
        </div>
      </div>
    </td>
    <td><b>${formatMoney(item.unit_price)}</b></td>
    <td>
      <div class="qty" aria-label="Quantity">
        <div class="btn-sm" onclick="changeQty(${item.id}, ${item.quantity - 1})">−</div>
        <input type="number" 
          value="${item.quantity}" 
          min="1" class="qty-input" 
          oninput="handleManualQty(${item.id},
          this.value)" />
        <div class="btn-sm" onclick="changeQty(${item.id}, ${item.quantity + 1})">+</div>
      </div>
    </td>
    <td><b>${formatMoney(item.line_total)}</b></td>
  </tr>
`).join("");
}

async function loadCart() {
  try {
    const cart = await fetchCart();
    renderCart(cart);
  } catch (error) {
    document.getElementById("cart-table-body").innerHTML = `
      <tr>
        <td colspan="4" class="empty-cart">Failed to load cart.</td>
      </tr>
    `;
    console.error(error);
  }
}

async function changeQty(itemId, newQty) {
  try {
    await updateItem(itemId, newQty);
    await loadCart();
  } catch (error) {
     showMessage(error.message, "error");
  }
}

async function handleRemove(itemId) {
  try {
    await deleteItem(itemId);
    await loadCart();
    showMessage("Item removed", "success");
  } catch (error) {
    showMessage("Could not remove item", "error");
  }
}

async function handleManualQty(itemId, value) {
  const qty = parseInt(value);

  if (isNaN(qty)) {
    showMessage("Invalid quantity", "error");
    return;
  }

  if (qty === 0) {
    try {
      await deleteItem(itemId);
      await loadCart();
      showMessage("Item removed", "success");
    } catch (error) {
      showMessage("Error removing item", "error");
    }
    return;
  }

  if (qty < 0) {
    showMessage("Invalid quantity", "error");
    return;
  }

  try {
    await updateItem(itemId, qty);
    await loadCart();
  } catch (error) {
    showMessage(error.message, "error")
  }
}

document.getElementById("clear-cart-btn").addEventListener("click", async function () {
  try {
    await clearCart();
    await loadCart();
  } catch (error) {
    console.error(error);
    alert("Could not clear cart.");
  }
});

loadCart();