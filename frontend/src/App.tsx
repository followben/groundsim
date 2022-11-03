import { AppShell, MantineProvider } from "@mantine/core";
import { ClientContext, GraphQLClient } from "graphql-hooks";
import { createClient } from "graphql-ws";

import Dashboard from "./Dashboard";
import Header from "./Header";

const client = new GraphQLClient({
  url: `${import.meta.env.VITE_API_SCHEME}://${import.meta.env.VITE_API_HOST}/graphql`,
  subscriptionClient: () =>
    createClient({
      url: `ws://${import.meta.env.VITE_API_HOST}/graphql`,
    }),
});

function App() {
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS theme={{ colorScheme: "dark" }}>
      <ClientContext.Provider value={client}>
        <AppShell
          padding="md"
          header={<Header />}
          styles={(theme) => ({
            main: { backgroundColor: theme.colorScheme === "dark" ? theme.colors.dark[8] : theme.colors.gray[0] },
          })}
        >
          <Dashboard />
        </AppShell>
      </ClientContext.Provider>
    </MantineProvider>
  );
}

export default App;
