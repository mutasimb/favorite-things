<template>
  <div id="app">
    <Header/>
    <Table/>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Table from "./components/Table.vue";

export default {
  name: "app",
  components: {
    Header,
    Table
  }
};
</script>

<style>
body {
  margin: 0;
  background-color: #f3f4f9;
  padding-bottom: 60px;
}

#app {
  font-family: "Nunito", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}
</style>
