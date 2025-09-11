const { VITE_API_HOST, VITE_API_PORT, VITE_MACHINE_IP } =
  import.meta.env;

export const settings = {
  API_HOST: VITE_API_HOST,
  API_PORT: Number(VITE_API_PORT),
  MACHINE_IP: VITE_MACHINE_IP ?? null
};

export const getAPIURL = () => `http://${settings.MACHINE_IP || settings.API_HOST}:${settings.API_PORT}/api`
