import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { MainWrapper } from "@/components/MainWrapper";
import { ChatWidget } from "@/components/ChatWidget";

export const metadata: Metadata = {
  title: {
    default: "VR Coatings Pvt. Ltd.",
    template: "%s | VR Coatings Pvt. Ltd.",
  },
  description:
    "Industrial coatings, protective systems, and specialty finishes from VR Coatings Pvt. Ltd.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
    <body className="flex min-h-screen flex-col bg-white antialiased">
      <Header />
      <MainWrapper>{children}</MainWrapper>
      <Footer />
      <ChatWidget />
    </body>
    </html>
  );
}
