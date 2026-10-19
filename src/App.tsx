// Provjera okruženja: frontend se pokreće, a backend i baza odgovaraju.
// Kad provjera prođe, zamijeni ovu komponentu svojom aplikacijom.
import { useEffect, useState } from "react";

export default function App() {
  const [baza, setBaza] = useState("Provjeravam bazu...");

  useEffect(() => {
    fetch("/api/provjera")
      .then((r) => r.json())
      .then((d: { poruka: string }) => setBaza(d.poruka))
      .catch(() => setBaza("Backend ne odgovara. Pogledaj greške [api] u terminalu."));
  }, []);

  return (
    <main style={{ padding: 32, fontFamily: "sans-serif", lineHeight: 1.6 }}>
      <h1>Aplikacija radi.</h1>
      <p>{baza}</p>
    </main>
  );
}
