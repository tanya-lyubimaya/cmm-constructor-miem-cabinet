<template>
  <div class="wrapper">
        <div class="navigation">
            <section class="container">
                <a class="navigation-title" href="/enter" title="База КИМов - Сервис для преподавателей МИЭМ НИУ ВШЭ">
                    <h1 class="title">База КИМов</h1>
                </a>
            </section>
        </div>
        <section class="container" id="base">
            <h3 class="title">База КИМов</h3>
            <a class="button button-outline" href="javascript:flipflop('enterNameOfCMM');">Создать КИМ</a>

            <div id="enterNameOfCMM">
              <el-form ref="form" :model="form" label-width="120px" id="cmm-name-form">
                  <el-form-item label="Название КИМа">
                    <el-input v-model="form.name" class="input" name="cmm-name"/>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" native-type="submit" @click="onSubmit">Create</el-button>
                    <el-button @click="onCancel">Cancel</el-button>
                  </el-form-item>
              </el-form>
            <!--
              <br>
                <form action="/main" method="post" novalidate>
                    {{ form.hidden_tag() }}
                        {{ form.cmm_name.label }}
                        {{ form.cmm_name(size=32) }}
                        {% for error in form.cmm_name.errors %}
                            <span style="color: red;">[{{ error }}]</span>
                        {% endfor %}
                    {{ form.submit() }}
                </form>
              {{ form.name(class="form-control", placeholder="Имя", **{'v-model':'user.name'}) }}-->
              <!--
                <el-form ref="form" :model="form" label-width="120px">
                  <el-form-item label="Activity name">
                    <el-input v-model="form.name"/>
                  </el-form-item>
                </el-form>
                -->
            </div>
            <br>
            <br><br><br>
            <h3 class="title">Мои курсы</h3>
        </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
      }
    }
  },
  methods: {
    onSubmit() {
      //this.$message('submit!')
      //this.$http.post('/api/something', JSON.stringify(this.form));
      this.$message(JSON.stringify(this.form.name))
      axios.post('http://127.0.0.1:5000/cmm-name', {
        cmm_name: this.name
      })
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>


<!--
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="http://code.jquery.com/jquery-2.0.2.min.js"></script>
<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
-->