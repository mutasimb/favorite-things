<template>
  <div class="row" @click="rowEdit">
    <div class="items">
      <p class="title">{{title}}</p>
      <p class="description" v-if="description != ''">{{description}}</p>
    </div>
    <div class="category">
      <p>{{transformCategory(category)}}</p>
    </div>
    <div class="rank">
      <p>{{rank}}</p>
    </div>
    <div class="created">
      <p>{{formatDateTime(created)}}</p>
    </div>
    <div class="updated">
      <p>{{formatDateTime(updated)}}</p>
    </div>
  </div>
</template>

<script>
import { utcParse, timeFormat } from "d3-time-format";
export default {
  name: "TableRow",
  props: {
    id: String,
    title: String,
    description: String,
    category: String,
    rank: Number,
    created: String,
    updated: String
  },
  data() {
    return {
      hovered: false,
      editMode: false
    };
  },
  methods: {
    rowEdit: function() {
      this.$emit("editHandler", this.id);
    },
    formatDateTime: function(str) {
      if (str.indexOf(".") > -1)
        str = str.replace(str.slice(str.indexOf(".")), "Z");
      return timeFormat("%B %-d, %Y, %-I:%M %p")(
        utcParse("%Y-%m-%dT%H:%M:%SZ")(str)
      );
    },
    transformCategory: function(str) {
      return str
        .split("_")
        .map(word => {
          let transformed = word.slice(0, 1).toUpperCase();
          if (word.length > 1) transformed += word.slice(1);
          return transformed;
        })
        .join(" ");
    }
  }
};
</script>

<style lang="scss" scoped>
.row {
  position: relative;
  margin: 0 auto;
  padding: 10px 0;
  min-height: 60px;
  max-width: 1200px;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  margin-left: -10px;
  margin-right: -10px;
  cursor: pointer;
  &:not(:last-child) {
    border-bottom: 1px solid #ebebeb;
  }
  &:first-child {
    border-top: 1px solid #ebebeb;
  }
  &:hover {
    background-color: rgba(#000000, 0.04);
  }
  p {
    font-size: 14px;
    margin-top: 0;
    margin-bottom: 0;
    color: #737488;
  }
  > :first-child {
    padding-left: 10px;
  }
  > :last-child {
    padding-right: 10px;
  }
  .items,
  .category,
  .rank,
  .created,
  .updated {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .items {
    width: 320px;
    text-align: left;
    .title {
      font-weight: 700;
      color: #819de3;
    }
    .description {
      color: #a0a0a7;
    }
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
  .btns {
    position: absolute;
    height: 100%;
    padding-left: 15px;
    top: 0;
    left: 100%;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    button {
      background: none;
      border: none;
      color: #78ae88;
      cursor: pointer;
      &:hover {
        color: #404a5c;
      }
    }
  }
}
</style>
