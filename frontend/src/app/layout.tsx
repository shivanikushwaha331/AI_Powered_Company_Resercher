import type { Metadata } from "next";
import "./globals.css";
import { ToastContainer } from "@/components/ui/toast";

export const metadata: Metadata = {
  title: "AI Company Research Assistant",
  description: "Production-grade AI company research assistant powered by FastAPI and Next.js",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="h-screen w-screen overflow-hidden flex flex-col bg-background text-foreground antialiased">
        {children}
        <ToastContainer />
      </body>
    </html>
  );
}
