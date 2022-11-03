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

const range = (start: number, stop: number, step: number) =>
  Array.from({ length: (stop - start) / step + 1 }, (_, i) => start + i * step);

const xTicks = (startDate: Date = new Date()) => {
  const start = Math.floor(startDate.getTime());
  const end = start + 360 * 1000;
  const result = range(start, end, 90 * 1000).map((x) => new Date(x));
  return result;
};

const yTicks = () => range(0, 45, 5);

interface Elevation {
  date: Date;
  value: number;
}

export default function ElevationChart() {
  const [elevations, setElevations] = useState<Elevation[]>([]);

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
    }
  });

  return (
    <VictoryChart containerComponent={<VictoryZoomContainer />} theme={VictoryTheme.grayscale}>
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
        dependentAxis
        style={{
          axis: { stroke: "#eee" },
          tickLabels: { fill: "#eee" },
          axisLabel: { fill: "#eee", padding: 35 },
        }}
        label="Elevation (m)"
        tickValues={yTicks()}
      />
      <VictoryLine
        style={{
          data: { stroke: "#eee" },
        }}
        data={elevations}
        x="date"
        y="value"
      />
    </VictoryChart>
  );
}
