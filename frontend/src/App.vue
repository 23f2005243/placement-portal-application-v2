<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
}
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

#app {
  width: 100vw;
  min-height: 100vh;
  background: #efe7ff; /* Light Purple */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: hidden;
  font-family: "Segoe UI", Arial, sans-serif;
}
</style>