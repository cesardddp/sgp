const App = {
    compilerOptions: {
        delimiters: ['@{', '}']
    },
    data() {
        return {
            cliente: {
                endereco: "",
                id: 1,
                nome: "",
                numero: null,
                projetos: [{
                        ambientes: [{
                                id: 1,
                                nome: "",
                                projeto_id: 1
                            },
                            {
                                id: 2,
                                nome: "",
                                projeto_id: 1
                            }
                        ],
                        data_apresentacao: null,
                        data_medicao: null,
                        id: 1,
                        usuario_id: 1
                    },
                    {
                        ambientes: [{
                            id: 9,
                            nome: "",
                            projeto_id: 6
                        }, ],
                        data_apresentacao: null,
                        data_medicao: "2021-10-15T03:00:00",
                        id: 6,
                        usuario_id: 1
                    }
                ],
                telefone: ""


            }
        }
    },
    methods: {

    },
    mounted() {
        return (
            axios
            .get(urlPegaCliente)
            .then(response => {
                // debugger
                this.cliente = response.data
            })
        )
    },
    computed: {
        // cliente() {
        //     return this.projeto.cliente.nome +
        //         " - " + this.projeto.cliente.endereco +
        //         " - " + this.projeto.cliente.telefone
        // },
    },


}
const app = Vue.createApp(App)
app.component('button-save', {

    props: ['field_name'],

    data() {
        return {
            save: true,
            loading: false,
            ready: false
        }
    },
    methods: {
        atualizar_projeto(field_name) {
            data = {}
            data[field_name] = this.$parent.projeto[field_name]
            // debugger
            axios
                .patch(urlPegaCliente, data)
                .then(response => {
                    if (response.status === 204) {
                        this.loading = false
                        this.ready = true
                    }
                })
                .catch(
                    function (error) {
                        console.log(error);
                    })
        },

    },
    template: `
    <button v-show="save" @click="save=!save,loading=true;atualizar_projeto(field_name)">
        <i class="fas fa-save"></i>
    </button>
    <i  v-show="loading" @click="loading=!loading,ready=true" class="fas fa-cog fa-spin"></i>
    <i  v-show="ready" @click="ready=!ready,save=true" class="fas fa-check"></i>
        `
})
app.mount("#app")