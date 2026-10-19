import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Narudžbe",
  description: "Praksa: aplikacija za narudžbe",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="bs">
      <body>{children}</body>
    </html>
  );
}
