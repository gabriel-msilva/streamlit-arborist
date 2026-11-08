import react from "@vitejs/plugin-react"
import process from "node:process"
import { defineConfig, UserConfig } from "vite"

export default defineConfig(() => {
  const isDev = process.env.NODE_ENV !== "production"

  return {
    base: "./",
    plugins: [react()],
    define: {
      // Library mode doesn't replace `process.env.NODE_ENV`, which React reads.
      "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV),
    },
    build: {
      minify: isDev ? false : "oxc",
      outDir: "build",
      sourcemap: isDev,
      lib: {
        entry: "./src/index.tsx",
        formats: ["es"],
        fileName: "index-[hash]",
      },
      rolldownOptions: {
        output: {
          // Hash the CSS file name too, so browsers don't cache it across versions.
          assetFileNames: "index-[hash][extname]",
        },
      },
    },
  } satisfies UserConfig
})
