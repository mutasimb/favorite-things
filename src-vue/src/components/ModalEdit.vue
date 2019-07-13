<template>
  <form @submit.prevent="handleSubmit">
    <div class="header">
      <div class="header-left">
        <h4 class="title">{{formData.pid ? `Edit Item: ${formData.title}` : "Add New Item"}}</h4>
      </div>
      <div class="header-right">
        <button
          type="button"
          class="cancel"
          @click="() => this.$emit(formData.pid ? 'cancel' : 'cancelForm')"
        >Cancel</button>
        <button type="submit" class="save">Save</button>
      </div>
    </div>
    <p v-if="errMessage" class="err-message">{{errMessage}}</p>
    <div class="primary-fields">
      <div class="form-group">
        <label for="title">Title</label>
        <input id="title" v-model="inputData.title" type="text" ref="title">
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="inputData.description"></textarea>
      </div>
      <div class="form-group">
        <label for="category">Category</label>
        <Multiselect
          id="category"
          v-model="inputData.category"
          :options="categoryOptions"
          :taggable="true"
          :allow-empty="false"
          placeholer="Category name"
          tag-placeholder="Add new category"
          @tag="newCategory"
        />
      </div>
      <div class="form-group">
        <label for="rank">Rank</label>
        <input id="rank" v-model="inputData.ranking" type="number">
      </div>
    </div>
    <template v-if="meta.length">
      <div v-for="(metaItem, i) in meta" :key="i" class="meta-fields">
        <div class="meta-header">
          <div class="header-left">
            <h4>Meta Field {{i+1}}</h4>
          </div>
          <div class="header-right">
            <button type="button" @click="removeMeta($event, i)">Remove</button>
          </div>
        </div>
        <div class="row">
          <div class="form-group">
            <label>Field Name</label>
            <input v-model="metaItem.key" type="text">
          </div>
          <div class="form-group">
            <label>Type</label>
            <select v-model="metaItem.type">
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="date">Date</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Value</label>
          <textarea v-if="metaItem.type == 'text'" v-model="metaItem.value"></textarea>
          <Datepicker v-else-if="metaItem.type == 'date'" v-model="metaItem.value"/>
          <input v-else v-model="metaItem.value" type="number">
        </div>
      </div>
    </template>
    <div class="btn-wrapper">
      <button type="button" class="btn-meta" @click="newMeta">Add another field</button>
    </div>
  </form>
</template>

<script>
import Multiselect from "vue-multiselect";
import Datepicker from "vuejs-datepicker";
import { timeFormat, timeParse } from "d3-time-format";

export default {
  data() {
    return {
      errMessage: "",
      inputData: {},
      meta: [],
      categoryOptions: ["people", "place", "food"]
    };
  },
  props: {
    formData: Object,
    categories: Array
  },
  components: {
    Multiselect,
    Datepicker
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
    reverseCategory: function(str) {
      return str.replace(" ", "_").toLowerCase();
    },
    transformDate: function(date) {
      return timeFormat("%Y%m%d")(date);
    },
    newCategory: function(cat) {
      this.categoryOptions.push(this.reverseCategory(cat));
      this.inputData.category = cat;
    },
    newMeta: function() {
      this.meta.push({
        key: "",
        type: "text",
        value: ""
      });
    },
    removeMeta: function(event, index) {
      this.meta = this.meta.filter((el, i) => i !== index);
    },
    handleSubmit: function() {
      this.errMessage = "";
      if (
        this.inputData.description.length > 0 &&
        this.inputData.description.length < 10
      ) {
        this.errMessage =
          "Description must be either blank, or have at least 10 characters.";
        return;
      }

      let submissionData = {};
      submissionData.title = this.inputData.title;
      submissionData.description = this.inputData.description;
      submissionData.category = this.reverseCategory(this.inputData.category);
      submissionData.ranking = this.inputData.ranking;
      submissionData.meta = JSON.stringify(
        this.meta.reduce((acc, el) => {
          return [
            ...acc,
            el.type == "date"
              ? { ...el, value: this.transformDate(el.value) }
              : el
          ];
        }, [])
      );

      this.$emit("formSubmission", submissionData);
    }
  },
  mounted() {
    let { category, description, ranking, title, meta } = this.formData;
    this.inputData = {
      category: this.transformCategory(category),
      description,
      ranking,
      title
    };
    this.categoryOptions = [...this.categoryOptions, ...this.categories]
      .filter((el, i, arr) => arr.indexOf(el) === i)
      .map(el => this.transformCategory(el));
    let parsedJson = JSON.parse(meta);
    if (parsedJson.length)
      this.meta = parsedJson.map(el => {
        if (el.type === "date") {
          let { value } = el,
            parsedDate = timeParse("%Y%m%d")(value),
            year = +timeFormat("%Y")(parsedDate),
            month = +timeFormat("%m")(parsedDate),
            day = +timeFormat("%d")(parsedDate),
            dateValue = new Date(year, month - 1, day);
          return { ...el, value: dateValue };
        } else {
          return el;
        }
      });
  }
};
</script>


<style lang="scss" scoped>
form {
  padding: 30px;
  button {
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
    &.save {
      margin-left: 5px;
    }
    &.btn-meta {
      margin-top: 15px;
    }
  }
  .err-message {
    margin-top: 0;
    margin-bottom: 0;
    color: red;
    font-size: 12px;
  }
  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 30px;
    .title {
      margin-top: 0;
      margin-bottom: 0;
    }
  }
  label {
    padding-top: 10px;
    font-weight: 700;
    font-size: 13px;
    color: #a0a0a7;
    margin-top: 0;
    margin-bottom: 0;
    width: 120px;
  }
  .primary-fields .form-group {
    display: flex;
    flex-direction: row;
    margin-top: 15px;
    input,
    textarea,
    .multiselect {
      flex: 1;
    }
    input,
    textarea {
      border-radius: 5px;
      border: 1px solid #e8e8e8;
    }
    input {
      min-height: 40px;
      padding-left: 13px;
      padding-right: 13px;
    }
    textarea {
      min-height: 80px;
    }
  }
  .meta-fields {
    margin-top: 15px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #e8e8e8;
    .meta-header,
    .row {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      h4 {
        margin-top: 0;
        margin-bottom: 0;
      }
    }
    .row {
      margin-top: 15px;
      margin-bottom: 15px;
      .form-group {
        width: calc(50% - 15px);
        input,
        select {
          flex: 1;
          border-radius: 5px;
          border: 1px solid #e8e8e8;
          min-height: 40px;
          background: none;
          background-color: white;
          padding-left: 5px;
          padding-right: 5px;
        }
      }
    }
    .form-group {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      label {
        width: 75px;
      }
      input,
      textarea,
      div {
        flex: 1;
      }
    }
  }
  .btn-wrapper {
    text-align: right;
  }
}
</style>
