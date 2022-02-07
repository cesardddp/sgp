const App = {
    compilerOptions: {
        delimiters: ['@{', '}']
    },
    data() {
        return {
            ultimo: 1,
            ambientes: [{
                nome: "",
                id: 1,
                label: "Ambiente 1"
            }],
            cliente: {
                nome: "",
                endereco: "",
                telefone: "",
                id: ""
            },
            data: "",
            hora: "",
            isButtonDisabled: true,

        }
    },
    methods: {
        add_amb() {
            this.ultimo = this.ultimo + 1
            this.ambientes.push({
                nome: "",
                id: this.ultimo,
                label: 'Ambiente ' + this.ultimo
            })
        },
        rm_amb() {
            if (this.ultimo == 1) {
                return
            }
            this.ultimo = this.ultimo - 1
            this.ambientes.pop()
        },
        novoProjeto() {

            const iso_data = new Date(
                this.data + ' ' + this.hora).toISOString();

            this.ambientes.forEach(element => {
                delete(element.id);
                delete(element.label)
            })
            let projeto = {
                usuario_id: 1,
                ambientes: this.ambientes,
                data_entrada: iso_data
            }
            if (!this.cliente.id) {
                let cliente = {
                    endereco: this.cliente.endereco,
                    nome: this.cliente.nome,
                    telefone: this.cliente.telefone,
                    numero: this.cliente.numero
                }
                projeto.cliente = cliente
            } else {
                projeto.cliente_id = this.cliente.id
            }
            axios
                .post(
                    endPointNovo, // load on jinja
                    projeto
                )
                .then(response => {
                    if (response.status === 200) {
                        location.pathname = endPointDetalhes + response.data
                            .projeto.id
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    mounted() {
        if (Preenchido) {
            this.cliente.nome = Cliente.nome
            this.cliente.endereco = Cliente.endereco
            this.cliente.telefone = Cliente.telefone
            this.cliente.id = Cliente.id
            this.cliente.numero = Cliente.numero
            }
        this.data = new Date().toISOString().split('T')[0]

        this.hora = new Date().toLocaleTimeString().slice(0, 5)
    },

}
var app = Vue.createApp(App)
app.use(Maska)
app.mount("#app")