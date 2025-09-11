import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";
import { configDotenv } from "dotenv";

configDotenv({ path: "../.env" });

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 6541, host: "0.0.0.0" },
  define: {
    "import.meta.env.VITE_API_HOST": JSON.stringify(process.env.API_HOST),
    "import.meta.env.VITE_API_PORT": JSON.stringify(process.env.API_PORT),
    "import.meta.env.VITE_MACHINE_IP": JSON.stringify(process.env.MACHINE_IP),
  },
});
