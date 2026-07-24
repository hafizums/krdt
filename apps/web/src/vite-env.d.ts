/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_KRDT_ENVIRONMENT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
