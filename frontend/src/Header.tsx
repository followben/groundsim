import { useState } from "react";

import { Button, Group, Header as MantineHeader } from "@mantine/core";
import { IconBuildingBroadcastTower } from "@tabler/icons";
import { useMutation, useSubscription } from "graphql-hooks";

const CREATE_SIMULATION_MUTATION = `mutation {
  createSimulation
}`;

const STATUS_SUBSCRIPTION = `subscription {
  running
}`;

enum ButtonState {
  Enabled = "Run",
  DisabledStarting = "Starting",
  DisabledRunning = "Running",
}

function Header() {
  const [buttonState, setButtonState] = useState(ButtonState.Enabled);
  const [createSimulation] = useMutation(CREATE_SIMULATION_MUTATION);
  useSubscription({ query: STATUS_SUBSCRIPTION }, ({ data, errors }) => {
    if (errors && errors.length > 0) {
      // eslint-disable-next-line no-console
      console.error(errors[0]);
      return;
    }
    setButtonState(data.running ? ButtonState.DisabledRunning : ButtonState.Enabled);
  });
  return (
    <MantineHeader height={60} p="xs">
      <Group sx={{ height: "100%" }} px={20} position="apart">
        <IconBuildingBroadcastTower size={16} />
        <Button
          onClick={async () => {
            setButtonState(ButtonState.DisabledStarting);
            await createSimulation();
          }}
          disabled={buttonState !== ButtonState.Enabled}
        >
          {buttonState}
        </Button>
      </Group>
    </MantineHeader>
  );
}

export default Header;
