<template>
  <div class="table-header">
    <div class="header">
      <div class="header-left">
        <h4 class="table-title">List of Favorite Things</h4>
      </div>
      <div class="header-right">
        <button @click="() => this.$emit('newItem')">Add New Item</button>
      </div>
    </div>
    <div class="head-row">
      <div
        v-for="(item, i) in columns"
        :key="item.className"
        :class="[item.className, { active: item.active }]"
        @click="columnClicked($event, i)"
      >
        <p>{{item.name + (item.type ? ` | ${item.type}` : "")}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    columns: Array
  },
  methods: {
    columnClicked: function(event, i) {
      this.$emit("columnClicked", i);
    }
  }
};
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  .table-title {
    margin: 0;
    font-size: 22px;
    line-height: 40px;
  }
  button {
    color: white;
    background: #4c8ffb;
    border: 1px #3079ed solid;
    box-shadow: inset 0 1px 0 #80b0fb;
    border-radius: 3px;
    height: 30px;
    font-family: "Nunito", sans-serif;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    &:hover {
      border: 1px #2f5bb7 solid;
      box-shadow: 0 1px 1px #eaeaea, inset 0 1px 0 #5a94f1;
      background: #3f83f1;
    }
    &:active {
      box-shadow: inset 0 2px 5px #2370fe;
    }
  }
}
.head-row {
  margin: 0 auto 10px;
  max-width: 1200px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  margin-left: -10px;
  margin-right: -10px;
  > div {
    cursor: pointer;
    &:hover p {
      color: #535468;
    }
  }
  > :first-child {
    padding-left: 10px;
  }
  > :last-child {
    padding-right: 10px;
  }
  .items {
    width: 320px;
    text-align: left;
  }
  .category {
    width: 120px;
    text-align: left;
  }
  .rank {
    width: 80px;
    text-align: right;
  }
  .created,
  .updated {
    width: 240px;
    text-align: right;
  }
  p {
    margin-top: 0;
    margin-bottom: 0;
    font-weight: 700;
    font-size: 14px;
    color: #a0a0a7;
    &::selection {
      color: #a0a0a7;
      background-color: transparent;
    }
  }
  .active p {
    color: #535468;
  }
}
</style>
