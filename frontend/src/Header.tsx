import { useState } from "react";

import { Button, Group, Header as MantineHeader } from "@mantine/core";
import { IconBuildingBroadcastTower } from "@tabler/icons";
import { useMutation } from "graphql-hooks";

const CREATE_SIMULATION_MUTATION = `mutation {
  createSimulation
}`;

function Header() {
  const [running, setRunning] = useState(false);
  const [createSimulation] = useMutation(CREATE_SIMULATION_MUTATION);
  return (
    <MantineHeader height={60} p="xs">
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
    </MantineHeader>
  );
}

export default Header;
