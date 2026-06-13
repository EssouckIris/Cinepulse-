import { motion } from "framer-motion";

export default function MovieCard({ movie }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-[#111] rounded-xl overflow-hidden shadow-lg border border-goldTheme cursor-pointer"
    >
      {/* Poster */}
      <div
        className="w-full h-52 flex items-center justify-center rounded-t-xl"
        style={{ background: "linear-gradient(135deg, #1a1a2e, #16213e)" }}
      >
        <span style={{ color: "#FFD700", fontSize: "13px", textAlign: "center", padding: "10px" }}>
          🎬 {movie.title}
        </span>
      </div>

      {/* Infos */}
      <div className="p-3">
        <h2 className="text-white font-bold text-sm truncate">{movie.title}</h2>
        <p className="text-yellow-400 text-xs mt-1">{movie.genre}</p>
      </div>
    </motion.div>
  );
}