import { useSubscription } from "graphql-hooks";
import { useState } from "react";
import { VictoryAxis, VictoryChart, VictoryLine, VictoryTheme, VictoryZoomContainer } from "victory";

const POINTS_SUBSCRIPTION = `
  subscription NewPoint {
    points {
      type
      timestamp
      value
    }
  }
`;

const STATUS_SUBSCRIPTION = `subscription {
  running
}`;

const range = (start: number, stop: number, step: number) =>
  Array.from({ length: (stop - start) / step + 1 }, (_, i) => start + i * step);

const xTicks = (startDate: Date = new Date()) => {
  const start = Math.floor(startDate.getTime());
  const end = start + 360 * 1000;
  const result = range(start, end, 90 * 1000).map((x) => new Date(x));
  return result;
};

interface Telemetry {
  date: Date;
  value: number;
}

export default function ElevationChart() {
  const [elevations, setElevations] = useState<Telemetry[]>([]);
  const [azimuths, setAzimuths] = useState<Telemetry[]>([]);

  function reset() {
    setElevations([]);
    setAzimuths([]);
  }

  useSubscription({ query: POINTS_SUBSCRIPTION }, ({ data, errors }) => {
    if (errors && errors.length > 0) {
      // eslint-disable-next-line no-console
      console.error(errors[0]);
      return;
    }
    const {
      points: { timestamp, value, type },
    } = data;
    if (type === "el") {
      setElevations((prev) => [...prev, { date: new Date(timestamp), value }]);
      // eslint-disable-next-line no-console
      console.log(elevations);
    } else if (type === "az") {
      setAzimuths((prev) => [...prev, { date: new Date(timestamp), value }]);
      // eslint-disable-next-line no-console
      console.log(azimuths);
    }
  });

  useSubscription({ query: STATUS_SUBSCRIPTION }, ({ data, errors }) => {
    if (errors && errors.length > 0) {
      // eslint-disable-next-line no-console
      console.error(errors[0]);
      return;
    }
    if (data.running) {
      reset();
    }
  });

  // https://formidable.com/open-source/victory/gallery/multiple-dependent-axes/

  return (
    <VictoryChart containerComponent={<VictoryZoomContainer />} theme={VictoryTheme.grayscale} domain={{ y: [0, 1] }}>
      <VictoryAxis
        style={{
          axis: { stroke: "#eee" },
          tickLabels: { fill: "#eee" },
          axisLabel: { fill: "#eee", padding: 35 },
        }}
        label="Time"
        tickValues={xTicks(elevations[0]?.date)}
        tickFormat={xTicks().map((t) => t.toLocaleTimeString([], { timeStyle: "short" }))}
      />
      <VictoryAxis
        key="el"
        dependentAxis
        style={{
          axis: { stroke: "#eee" },
          tickLabels: { fill: "#eee" },
          axisLabel: { fill: "#eee", padding: 35 },
        }}
        label="Elevation"
        tickValues={[0.111, 0.222, 0.333, 0.444, 0.555, 0.666, 0.777, 0.888, 0.999]}
        tickFormat={[5, 10, 15, 20, 25, 30, 35, 40, 45]}
      />
      <VictoryLine
        key="el"
        style={{
          data: { stroke: "#eee" },
        }}
        data={elevations}
        x="date"
        y={(el) => el.value / 45}
      />
      <VictoryAxis
        key="az"
        dependentAxis
        orientation="right"
        offsetX={50}
        style={{
          axis: { stroke: "orange" },
          tickLabels: { fill: "orange" },
          axisLabel: { fill: "orange", padding: 35 },
        }}
        label="Azimuth"
        tickValues={[0.25, 0.5, 0.75, 1]}
        tickFormat={(t) => t * 360}
      />
      <VictoryLine
        key="az"
        style={{
          data: { stroke: "orange" },
        }}
        data={azimuths}
        x="date"
        y={(az) => az.value / 360}
      />
    </VictoryChart>
  );
}
