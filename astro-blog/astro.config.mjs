import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  site: "https://example.com", // TODO: ドメイン決定後に変更
  integrations: [tailwind()],
  output: "static",
});
