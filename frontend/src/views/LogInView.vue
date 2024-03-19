
<script>
    export default {
        name: 'LogIn',
        data() {
            return {
                showPassword: false,
            }
        },
    }

</script>


<template>
    <v-container>
        <div>
            <v-card width="400" class="mx-auto">
            <v-card-title> Welcome stranger </v-card-title>
            <v-card-text>
                By all means, this is just a personal space where I look into  topics of interest.
                A working progress to explore the different components that used in regard to machine learning/AI Engineering
                
            </v-card-text>
            </v-card>
        </div>

        <div id = "login">
            <!-- loginmodule -->
            <v-card width="400" class="mx-auto">
                <v-card-title>
                <h1 class="display-1">Login</h1>
                </v-card-title>
                <v-card-text>
                <v-form>
                    <v-text-field 
                        label = "Username" 
                        prepend-icon = "mdi-account-circle"/>
                    <v-text-field
                        :type = "showPassword ? 'text' : 'password'"
                        label = "Password"
                        icon = "fa:fas fa-lock"
                        :append-icon = "showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append = "showPassword = !showPassword"
                    />
                </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                <v-btn color="success">Register</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="info">Login</v-btn>
                </v-card-actions>
            </v-card>
        </div>

        <div>
            <v-card width="400" class="mx-auto">
            <v-card-text>
               This is for personal use.
            </v-card-text>
            </v-card>
        </div>

    </v-container>
</template>


<style scoped>

</style>