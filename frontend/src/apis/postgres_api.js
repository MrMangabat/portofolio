import axios from "axios"

const apiPostgres = axios.create({
    baseURL: "http://127.0.0.1:8000/",
    withCredentials: false,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
    }
})

export default {
    getWorkingExperiences() {
        return apiPostgres.get("/get-working-experiences")
    },
    getEducation() {
        return apiPostgres.get("/get-education")
    }
}
