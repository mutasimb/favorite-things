<template>
  <div class="table">
    <TableHeader :columns="columns" @newItem="newItem" @columnClicked="handleColumnClicked"/>
    <div class="body-row">
      <TableRow
        v-for="el in sort"
        :key="el.pid"
        :id="el.pid"
        :title="el.title"
        :description="el.description"
        :category="el.category"
        :rank="el.ranking"
        :created="el.created_at"
        :updated="el.updated_at"
        @editHandler="handleEditRow"
      />
    </div>
    <Modal
      v-if="(modalData && Object.keys(modalData).length > 0)"
      :categories="categories"
      :formData="modalData"
      @closeModalWithoutSaving="closeModalHandler"
      @formSubmission="handleFormSubmission"
      @deleteHandler="deleteItem"
    />
  </div>
</template>

<script>
import axios from "axios";
import { timeFormat, utcParse } from "d3-time-format";

import TableHeader from "./TableHeader.vue";
import TableRow from "./TableRow.vue";
import Modal from "./Modal.vue";

export default {
  name: "Data",
  components: {
    TableHeader,
    TableRow,
    Modal
  },
  data() {
    return {
      jsonData: [],
      modalData: {},
      categories: [],
      columns: [
        { className: "items", name: "Favorite Things" },
        { className: "category", name: "Category", active: true, type: "Asc" },
        { className: "rank", name: "Rank", active: true, type: "Asc" },
        { className: "created", name: "Created Date" },
        { className: "updated", name: "Updated Date" }
      ]
    };
  },
  computed: {
    sort: function() {
      let { jsonData } = this;
      let active = this.columns.filter(el => el.active);

      if (!active.length) {
        return jsonData;
      } else if (active.length == 2) {
        let typeCategory = active[0].type;
        let typeRank = active[1].type;

        return jsonData.sort((a, b) => {
          if (a.category === b.category) {
            return typeRank === "Desc"
              ? a.ranking > b.ranking
                ? -1
                : 1
              : a.ranking > b.ranking
              ? 1
              : -1;
          } else {
            return typeCategory === "Desc"
              ? a.category > b.category
                ? -1
                : 1
              : a.category > b.category
              ? 1
              : -1;
          }
        });
      } else {
        let { className, type } = active[0];
        if (className === "items") {
          return jsonData.sort((a, b) =>
            type === "Desc"
              ? a.title > b.title
                ? -1
                : 1
              : a.title > b.title
              ? 1
              : -1
          );
        } else {
          return jsonData.sort((a, b) =>
            type === "Desc"
              ? this.formatDateTime(a[`${className}_at`]) >
                this.formatDateTime(b[`${className}_at`])
                ? -1
                : 1
              : this.formatDateTime(a[`${className}_at`]) >
                this.formatDateTime(b[`${className}_at`])
              ? 1
              : -1
          );
        }
      }
    }
  },
  methods: {
    validateRanking: function(cat, rank, method) {
      let categoryItems = this.jsonData.filter(el => el.category === cat)
        .length;

      return rank < 1
        ? 1
        : rank > categoryItems
        ? method === "post"
          ? categoryItems + 1
          : categoryItems
        : rank;
    },
    handleColumnClicked: function(i) {
      this.columns = this.columns.map((el, index) =>
        i == 1 || i == 2
          ? {
              ...el,
              active: index === 1 || index === 2 ? true : false,
              type:
                index === 1 || index === 2
                  ? !el.active
                    ? "Asc"
                    : index === i
                    ? el.type !== "Asc"
                      ? "Asc"
                      : "Desc"
                    : el.type
                  : ""
            }
          : {
              ...el,
              active: index === i ? true : false,
              type: index === i ? (el.type !== "Asc" ? "Asc" : "Desc") : ""
            }
      );
    },
    handleFormSubmission: function(value) {
      let { title, description, category, ranking, meta } = value;

      if (value.id) {
        let putData = {
          title,
          description,
          category,
          ranking: this.validateRanking(category, +ranking, "put"),
          meta
        };
        axios
          .put(`/api/favorite-things/${value.id}`, putData)
          .then(res => {
            this.updateJson();
            this.closeModalHandler();
          })
          .catch(err => {
            console.log(err);
          });
      } else {
        let postData = {
          title,
          description,
          category,
          ranking: this.validateRanking(category, +ranking, "post"),
          meta
        };
        axios
          .post("/api/favorite-things/", postData)
          .then(res => {
            this.updateJson();
            this.closeModalHandler();
          })
          .catch(err => {
            console.log(err);
          });
      }
    },
    formatDateTime: function(str) {
      if (str.indexOf(".") > -1)
        str = str.replace(str.slice(str.indexOf(".")), "Z");
      return +timeFormat("%Y%m%d%H%M%S")(utcParse("%Y-%m-%dT%H:%M:%SZ")(str));
    },
    deleteItem: function(id) {
      axios
        .delete(`/api/favorite-things/${id}`)
        .then(() => {
          this.updateJson();
          this.closeModalHandler();
        })
        .catch(err => {
          return err;
        });
    },
    closeModalHandler: function() {
      this.modalData = {};
    },
    handleEditRow: function(id) {
      this.modalData = this.jsonData.filter(el => el.pid === id)[0];
    },
    newItem: function() {
      this.modalData = {
        title: "",
        description: "",
        category: "",
        ranking: "",
        meta: "[]"
      };
    },
    updateJson: function() {
      axios
        .get("/api/favorite-things")
        .then(res => {
          this.jsonData = res.data.favorite_things;
          this.categories = this.jsonData.reduce(
            (acc, el) =>
              acc.indexOf(el.category) > -1 ? acc : [...acc, el.category],
            []
          );
        })
        .catch(() => {
          this.jsonError = true;
        });
    }
  },
  mounted: function() {
    this.updateJson();
  }
};
</script>

<style lang="scss" scoped>
.table {
  margin: 75px auto 0;
  padding: 30px 60px;
  max-width: 1200px;
  background: #fdfdfc;
  position: relative;
  -webkit-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3),
    0 0 40px rgba(0, 0, 0, 0.1) inset;
  -moz-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3),
    0 0 40px rgba(0, 0, 0, 0.1) inset;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3), 0 0 40px rgba(0, 0, 0, 0.1) inset;
  &::before,
  &::after {
    content: "";
    position: absolute;
    z-index: -1;
    -webkit-box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    -moz-box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    top: 50%;
    bottom: 0;
    left: 10px;
    right: 10px;
    -moz-border-radius: 100px / 10px;
    border-radius: 100px / 10px;
  }
}
</style>
