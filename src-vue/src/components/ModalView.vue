<template>
  <div class="modal-view">
    <div class="header">
      <div class="header-left">
        <h4 class="title">{{formData.title}}</h4>
      </div>
      <div class="header-right">
        <button class="edit" @click="() => this.$emit('edit')">Edit</button>
        <button class="delete" @click="() => this.$emit('delete')">Delete</button>
      </div>
    </div>
    <div class="attributes">
      <div class="row">
        <div class="attribute-category">
          <p class="key">Category</p>
          <p class="value">{{transformCategory(formData.category)}}</p>
        </div>
        <div class="attribute-rank">
          <p class="key">Rank</p>
          <p class="value">{{formData.ranking}}</p>
        </div>
      </div>
      <div class="attribute-description">
        <p class="key">Description</p>
        <p class="value">{{formData.description}}</p>
      </div>
      <div class="row-date">
        <div class="attribute-created">
          <p class="key">Created</p>
          <p class="value">{{formatDateTime(formData.created_at)}}</p>
        </div>
        <div class="attribute-updated">
          <p class="key">Updated</p>
          <p class="value">{{formatDateTime(formData.updated_at)}}</p>
        </div>
      </div>
      <template v-if="meta.length">
        <div v-for="(item, i) in meta" :key="i" class="attribute-meta">
          <p class="key">{{item.key}}</p>
          <p class="value">{{item.value}}</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { utcParse, timeParse, timeFormat } from "d3-time-format";

export default {
  data() {
    return {
      meta: []
    };
  },
  props: {
    formData: Object
  },
  methods: {
    transformCategory: function(str) {
      return str
        .split("_")
        .map(word => {
          let transformed = word.slice(0, 1).toUpperCase();
          if (word.length > 1) transformed += word.slice(1);
          return transformed;
        })
        .join(" ");
    },
    formatDateTime: function(str) {
      if (str.indexOf(".") > -1)
        str = str.replace(str.slice(str.indexOf(".")), "Z");
      return timeFormat("%B %-d, %Y, %-I:%M %p")(
        utcParse("%Y-%m-%dT%H:%M:%SZ")(str)
      );
    }
  },
  mounted() {
    this.meta = JSON.parse(this.formData.meta).map(el =>
      el.type === "date"
        ? {
            ...el,
            value: timeFormat("%B %-d, %Y")(timeParse("%Y%m%d")(el.value))
          }
        : el
    );
  }
};
</script>


<style lang="scss" scoped>
.modal-view {
  padding: 30px;
}
.header {
  margin-bottom: 30px;
  .title {
    margin-top: 0;
    margin-bottom: 0;
  }
  .edit,
  .delete {
    color: #444444;
    background: #f3f3f3;
    border: 1px #dadada solid;
    padding: 5px 10px;
    border-radius: 2px;
    font-weight: bold;
    font-size: 9pt;
    outline: none;
    &:hover {
      border: 1px #c6c6c6 solid;
      box-shadow: 1px 1px 1px #eaeaea;
      color: #333333;
      background: #f7f7f7;
    }
    &:active {
      box-shadow: inset 1px 1px 1px #dfdfdf;
    }
  }
  .delete {
    margin-left: 5px;
  }
}
.header,
.row,
.row-date {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.attribute-category,
.attribute-rank,
.attribute-created,
.attribute-updated {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: calc(50% - 30px);
}
.attribute-description,
.attribute-meta {
  display: flex;
  .value {
    flex: 1;
    text-align: justify;
    font-size: 13px;
    color: #737488;
  }
}
.attribute-description,
.attribute-meta,
.row-date {
  margin-top: 15px;
}

.key {
  font-weight: 700;
  font-size: 13px;
  color: #a0a0a7;
  margin-top: 0;
  margin-bottom: 0;
  width: 120px;
}
.value {
  margin-top: 0;
  margin-bottom: 0;
  .attribute-category &,
  .attribute-rank & {
    font-weight: 700;
    font-size: 14px;
    color: #819de3;
  }
  .attribute-created &,
  .attribute-updated & {
    font-size: 13px;
    color: #737488;
  }
}
</style>
