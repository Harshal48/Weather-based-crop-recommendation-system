document.getElementById("cropForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
      });

      const result = await res.json();
      document.getElementById("result").innerText =
          result.recommended_crop
              ? "✅ Recommended Crop: " + result.recommended_crop
              : "❌ Error: " + result.error;
  } catch (error) {
      document.getElementById("result").innerText = "❌ Could not connect to server.";
  }
});
