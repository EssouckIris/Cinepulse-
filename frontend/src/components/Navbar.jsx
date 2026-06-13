export default function Navbar() {
  return (
    <nav className="bg-blackTheme border-b border-goldTheme px-10 py-4 flex items-center justify-between">
      <h1 style={{ color: "#FFD700", fontSize: "2.5rem", fontWeight: "bold", letterSpacing: "0.1em" }}>
        🎬 CinePulse
      </h1>
      <p className="text-gray-400 text-sm italic">
        Recommandations intelligentes
      </p>
    </nav>
  );
}