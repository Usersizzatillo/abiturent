// `output: "standalone"` makes `next start` fail outright ("next start does not
// work with output: standalone"), so `npm start` has to run the generated
// server.js. That server only serves assets that sit next to it, which means
// `.next/static` and `public/` have to be copied inside `.next/standalone`.
//
// The Dockerfile does the same copy in its own build stage; running this after
// every build keeps `npm start` working outside a container too.
import { cp, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const root = process.cwd();
const standalone = path.join(root, ".next", "standalone");

if (!existsSync(standalone)) {
  console.error(
    "[prepare-standalone] .next/standalone not found — run `npm run build` first."
  );
  process.exit(1);
}

const copies = [
  [path.join(root, ".next", "static"), path.join(standalone, ".next", "static")],
  [path.join(root, "public"), path.join(standalone, "public")],
];

for (const [from, to] of copies) {
  if (!existsSync(from)) continue;
  await mkdir(path.dirname(to), { recursive: true });
  await cp(from, to, { recursive: true });
}

console.log("[prepare-standalone] copied static assets into .next/standalone");
