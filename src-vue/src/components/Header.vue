<template>
  <header id="header">
    <div class="header">
      <div class="header-left">
        <p>
          <b>BriteCore</b>
          <span>|</span>Software Engineer Hiring Test
        </p>
      </div>
      <div class="header-right">
        <a href="https://github.com/mutasimb/favorite-things" target="_blank">GitHub</a>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
#header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: -1;
  width: 100%;
  height: 200px;
  background-color: #424155;
  color: white;
  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 0 auto;
    max-width: 1200px;
    p {
      margin: 0;
      line-height: 75px;
      b {
        letter-spacing: 1px;
      }
      span {
        margin: 0 10px;
      }
    }
    a {
      margin: 0;
      line-height: 75px;
      color: inherit;
    }
  }
}
</style>

