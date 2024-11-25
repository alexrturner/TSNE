<script>
  import * as d3 from "d3";
  import io from "socket.io-client";
  import { onMount } from "svelte";
  let clientWidth = window.innerWidth;
  let clientHeight = window.innerHeight;
  let svg;
  let data = [];
  let width = clientWidth - 40;
  let height = clientHeight - 60;
  let margin = { top: 20, right: 20, bottom: 30, left: 20 };

  onMount(() => {
    console.log("Component mounted");

    svg = d3
      .select("#graph")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // zoom functionality
    const zoom = d3.zoom().scaleExtent([0.5, 5]);
    // .on("zoom", (event) => {
    //   svg.attr("transform", event.transform);
    // });

    d3.select("#graph svg").call(zoom);

    const socket = io("http://localhost:5000");

    socket.on("connect", () => {
      console.log("Connected to server");
    });

    socket.on("update", (newData) => {
      console.log("Received update:", newData);
      data = newData;
      updategraph();
    });

    // fetch initial data
    fetch("http://localhost:5000/data")
      .then((response) => response.json())
      .then((initialData) => {
        console.log("Initial data received:", initialData);
        data = initialData;
        updategraph();
      })
      .catch((error) => console.error("Error fetching data:", error));
  });

  function getDataUrl(path) {
    // Remove any leading './' or '/' from the path
    const cleanPath = path.replace(/^\.?\//, "");
    return `http://localhost:5000/data/${encodeURIComponent(cleanPath)}`;
  }

  function updategraph() {
    console.log("Updating graph with data:", data);

    if (!svg || data.length === 0) return;

    // Create scales
    const xScale = d3
      .scaleLinear()
      .domain(d3.extent(data, (d) => d.x))
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain(d3.extent(data, (d) => d.y))
      .range([height, 0]);

    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    // update circles
    const circles = svg.selectAll("circle").data(data, (d) => d.path);

    circles
      .enter()
      .append("a")
      .attr("href", (d) => getDataUrl(d.path))
      .attr("target", "_blank")
      .append("circle")
      .attr("r", 5)
      .attr("fill", "olive")
      .merge(circles)
      .attr("cx", (d) => xScale(d.x))
      .attr("cy", (d) => yScale(d.y))
      .on("mouseover", (event, d) => {
        svg
          .selectAll(".label")
          .filter((label) => label.path === d.path)
          .transition()
          // .duration(100)
          .style("opacity", 1);
      })
      .on("mouseout", () => {
        svg.selectAll(".label").transition().duration(500).style("opacity", 0);
      });

    circles.exit().remove();

    // update labels
    const labels = svg.selectAll("text").data(data, (d) => d.path);

    labels
      .enter()
      .append("a")
      .attr("href", (d) => getDataUrl(d.path))
      .attr("target", "_blank")
      .append("text")
      .attr("dx", 8)
      .attr("dy", ".35em")
      .attr("class", "label")
      .style("opacity", 0)
      .merge(labels)
      .attr("x", (d) => xScale(d.x))
      .attr("y", (d) => yScale(d.y))
      .text((d) => d.title);

    labels.exit().remove();

    // Add axes
    // svg.selectAll(".axis").remove();

    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${height})`);

    svg.append("g").attr("class", "axis").call(d3.axisLeft(yScale));
    svg.append("g").attr("class", "axis").call(d3.axisTop(xScale));
  }
</script>

<main>
  <div id="graph"></div>
  <h1>there are {data.length} files</h1>
</main>

<style>
  :global(.axis path, .axis line) {
    stroke: #ccc;
  }

  :global(.axis text) {
    fill: #666;
  }
</style>
