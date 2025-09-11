const { VITE_API_HOST, VITE_API_PORT } =
  import.meta.env;

export const settings = {
  API_HOST: VITE_API_HOST,
  API_PORT: Number(VITE_API_PORT),
};

export const getAPIURL = () => `http://${settings.API_HOST}:${settings.API_PORT}/api`
