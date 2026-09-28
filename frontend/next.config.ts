import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  // Next strips trailing slashes by default (308), but the Django API is
  // slash-terminated: without this, POST /api/auth/login/ becomes POST
  // /api/auth/login and Django raises "APPEND_SLASH can't redirect a POST".
  skipTrailingSlashRedirect: true,
  turbopack: {
    root: __dirname,
  },
  async rewrites() {
    // `:path*` captures segments without the trailing slash, so it is added
    // back explicitly here (nginx passes the original URI untouched).
    return [{ source: "/api/:path*", destination: `${backendUrl}/api/:path*/` }];
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
      { protocol: "https", hostname: "randomuser.me" },
    ],
  },
};

export default withNextIntl(nextConfig);