<template>
  <div id="app">
    <div class="container" style="width:600px">

     <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <div class="container">
        <span class="navbar-brand">Cow Recognition System</span>
      </div>
    </nav>
      <br>   
      <br>
      <div style="margin: 20px">
        <br>
        <h4>Please upload an image</h4>
      </div>

      <upload-files></upload-files>
    </div>
  </div>
</template>

<script>
import UploadFiles from "./components/UploadFiles";

export default {
  name: "App",
  components: {
    UploadFiles
  }
};
</script>
