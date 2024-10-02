// Django 後端 API 位址
const API_BASE_URL = "http://localhost:8000";

const output = document.getElementById("output");

async function getOTP() {
  const username = document.getElementById("username").value;
  if (!username) {
    output.innerHTML = "Please enter username";
    return;
  }
  try {
    const response = await fetch(`${API_BASE_URL}/otp/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username }),
      credentials: "include",
    });

    const otpRespData = await response.json();

    output.innerHTML = "OTP send successfully";
  } catch (error) {
    output.innerHTML = `Error: ${error.message}`;
  }
}

async function getToken() {
  const username = document.getElementById("username").value;
  const otp = document.getElementById("otp").value;

  if (!username || !otp) {
    output.innerHTML = "Please enter username and OTP";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, otp: otp }),
      credentials: "include",
    });

    const tokenRespData = await response.json();

    if (tokenRespData.access) {
      // Store the access token in localStorage
      localStorage.setItem("accessToken", tokenRespData.access);
      output.innerHTML =
        "Successfully got tokens. Access token stored in localStorage.";
    } else {
      output.innerHTML = "Access token not received from the server.";
    }

    // Note: The refresh token should be automatically stored as an HttpOnly cookie by the server
  } catch (error) {
    output.innerHTML = `Error: ${error.message}`;
  }
}

async function accessProtectedResource() {
  async function fetchWithToken(token) {
    const response = await fetch(`${API_BASE_URL}/protected/`, {
      method: "GET",
      credentials: "include",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw response;
    }
    return response.json();
  }

  try {
    // 首先嘗試使用存儲的 access token
    let accessToken = localStorage.getItem("accessToken");

    try {
      const data = await fetchWithToken(accessToken);
      output.innerHTML = `Protected Resource: ${JSON.stringify(data)}`;
    } catch (error) {
      if (error.status === 401) {
        // Token 可能已過期，嘗試刷新
        accessToken = await refreshAccessToken();
        // 使用新的 token 重試
        const data = await fetchWithToken(accessToken);
        output.innerHTML = `Protected Resource (after refresh): ${JSON.stringify(
          data
        )}`;
      } else {
        throw error;
      }
    }
  } catch (error) {
    console.error("Error accessing protected resource:", error);
    output.innerHTML = `Error: ${
      error.message || "Failed to access protected resource"
    }`;
  }
}

async function refreshAccessToken() {
  try {
    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
      method: "POST",
      credentials: "include", // 重要：允許發送和接收 cookies
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    if (!response.ok) {
      throw new Error("Failed to refresh token");
    }
    const data = await response.json();
    if (data.access) {
      localStorage.setItem("accessToken", data.access);
      output.innerHTML = "Token refreshed successfully";
    } else {
      throw new Error("No access token received");
    }
  } catch (error) {
    console.error("Error refreshing token:", error);
    throw error;
  }
}

async function debugRequest() {
  try {
    const response = await fetch(`${API_BASE_URL}/debug/`, {
      method: "GET",
      credentials: "include",
    });
    const data = await response.json();
    output.innerHTML = `Debug response: ${JSON.stringify(data)}`;
  } catch (error) {
    console.error("Debug request error:", error);
  }
}
