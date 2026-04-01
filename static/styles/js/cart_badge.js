async function loadCartBadge() {
  try {
    const response = await fetch("/cart/api/");
    const data = await response.json();

    const badge = document.getElementById("cart-badge");
    if (badge) {
      badge.textContent = data.total_items || 0;
    }
  } catch (e) {
    console.error("Failed to load cart badge");
  }
}

document.addEventListener("DOMContentLoaded", loadCartBadge);