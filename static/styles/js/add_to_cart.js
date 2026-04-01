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

async function addToCartById(productId) {
    const response = await fetch("/cart/api/items/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        product_id: productId,
        quantity: 1
      })
    });

    let data;

    try {
      data = await response.json();
    } catch {
      showMessage("Server error", "error");
      return;
    }

    if (!response.ok) {
      showMessage(data.error || data.detail || "Error", "error");
      return;
    }

    showMessage("Item added to basket", "success");
    await loadCartBadge();
}
