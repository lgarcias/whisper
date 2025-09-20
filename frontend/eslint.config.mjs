// frontend/eslint.config.mjs
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  // Configs base de Next + TS
  ...compat.extends("next/core-web-vitals", "next/typescript"),

  // Ignorados comunes en Next
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "build/**",
      "coverage/**",
      "next-env.d.ts",
    ],
  },

  // Reglas ajustadas para un flujo de trabajo más fluido
  {
    rules: {
      // Permite prototipar pero te avisa
      "@typescript-eslint/no-explicit-any": "warn",

      // No bloquea por variables no usadas; ignora args que empiezan por "_"
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],

      // Innecesario en Next.js
      "react/react-in-jsx-scope": "off",

      // Útil como aviso, no como error duro
      "react/jsx-key": "warn",

      // Permite console.warn/error sin ruido
      "no-console": ["warn", { allow: ["warn", "error"] }],

      // Común en pages/api y componentes de Next
      "import/no-anonymous-default-export": "off",
    },
  },
];

export default eslintConfig;
