import { AppShell, Button, Group, Header, MantineProvider } from "@mantine/core";
import { IconBuildingBroadcastTower } from "@tabler/icons";
import { ClientContext, GraphQLClient, useMutation } from "graphql-hooks";
import { useState } from "react";

const CREATE_SIMULATION_MUTATION = `mutation {
  createSimulation
}`;

const client = new GraphQLClient({
  url: `${import.meta.env.VITE_API_HOST}/graphql`,
});

function Dashboard() {
  return (
    <div>
      <h1>Groundsim</h1>
    </div>
  );
}

function Demo() {
  const [running, setRunning] = useState(false);
  const [createSimulation] = useMutation(CREATE_SIMULATION_MUTATION);
  return (
    <AppShell
      padding="md"
      header={
        <Header height={60} p="xs">
          <Group sx={{ height: "100%" }} px={20} position="apart">
            <IconBuildingBroadcastTower size={16} />
            <Button
              onClick={async () => {
                const {
                  data: { createSimulation: success },
                } = await createSimulation();
                setRunning(success);
              }}
              disabled={running}
            >
              {running ? "Running" : "Run"}
            </Button>
          </Group>
        </Header>
      }
      styles={(theme) => ({
        main: { backgroundColor: theme.colorScheme === "dark" ? theme.colors.dark[8] : theme.colors.gray[0] },
      })}
    >
      <Dashboard />
    </AppShell>
  );
}

function App() {
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS theme={{ colorScheme: "dark" }}>
      <ClientContext.Provider value={client}>
        <Demo />
      </ClientContext.Provider>
    </MantineProvider>
  );
}

export default App;
