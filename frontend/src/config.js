async function loadConfig() {
    try {
      const response = await fetch("http://localhost:8080/frontend-config");
      if (!response.ok) {
        throw new Error("Failed to load config");
      }
      const config = await response.json();
      return config;
    } catch (error) {
      console.error("Error loading config:", error);
      return {}; // Return empty config if there's an error
    }
  }
  
  export default loadConfig;
  