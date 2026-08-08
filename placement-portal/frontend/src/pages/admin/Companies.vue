<template>

  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>Companies</h2>

      <div class="d-flex gap-2">

        <input
          v-model="search"
          type="text"
          class="form-control"
          placeholder="Search companies..."
          @keyup.enter="searchCompanies"
        />

        <button
          class="btn btn-primary"
          @click="searchCompanies"
        >
          Search
        </button>

      </div>

    </div>


    <div class="card shadow-sm">

      <div class="card-body">

        <div class="table-responsive">

          <table class="table table-hover">

            <thead>

              <tr>

                <th>Company</th>

                <th>Email</th>

                <th>HR</th>

                <th>Approval</th>

                <th>Account</th>

                <th>Actions</th>

              </tr>

            </thead>


            <tbody>

              <tr
                v-for="company in companies"
                :key="company.id"
              >

                <td>
                  {{ company.company_name }}
                </td>

                <td>
                  {{ company.email }}
                </td>

                <td>
                  {{ company.hr_name || "-" }}
                </td>

                <td>

                  <span
                    class="badge"
                    :class="
                      company.approval_status === 'approved'
                        ? 'bg-success'
                        : 'bg-warning text-dark'
                    "
                  >
                    {{ company.approval_status }}
                  </span>

                </td>

                <td>

                  <span
                    v-if="company.is_active"
                    class="badge bg-success"
                  >
                    Active
                  </span>

                  <span
                    v-else
                    class="badge bg-danger"
                  >
                    Inactive
                  </span>

                </td>

                <td>

                  <button
                    v-if="company.is_active"
                    class="btn btn-sm btn-warning me-1"
                    @click="deactivateCompany(company.id)"
                  >
                    Deactivate
                  </button>

                  <button
                    v-else
                    class="btn btn-sm btn-success me-1"
                    @click="activateCompany(company.id)"
                  >
                    Activate
                  </button>


                  <button
                    v-if="!company.is_blacklisted"
                    class="btn btn-sm btn-danger"
                    @click="blacklistCompany(company.id)"
                  >
                    Blacklist
                  </button>

                  <button
                    v-else
                    class="btn btn-sm btn-secondary"
                    @click="unblacklistCompany(company.id)"
                  >
                    Remove Blacklist
                  </button>

                </td>

              </tr>


              <tr v-if="companies.length === 0">

                <td
                  colspan="6"
                  class="text-center text-muted"
                >

                  No companies found.

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue";

import api from "../../services/api";


const companies = ref([]);

const search = ref("");


async function searchCompanies() {

  try {

    const response = await api.get(
      "/admin/companies/search",
      {
        params: {
          q: search.value
        }
      }
    );

    companies.value = response.data;

  } catch (error) {

    console.error(error);

    alert(
      error?.response?.data?.message ||
      "Failed to load companies."
    );

  }

}


async function deactivateCompany(id) {

  if (!confirm(
    "Deactivate this company?"
  )) {
    return;
  }

  try {

    await api.put(
      `/admin/companies/${id}/deactivate`
    );

    await searchCompanies();

  } catch (error) {

    alert(
      error?.response?.data?.message ||
      "Failed to deactivate company."
    );

  }

}


async function activateCompany(id) {

  try {

    await api.put(
      `/admin/companies/${id}/activate`
    );

    await searchCompanies();

  } catch (error) {

    alert(
      error?.response?.data?.message ||
      "Failed to activate company."
    );

  }

}


async function blacklistCompany(id) {

  if (!confirm(
    "Blacklist this company?"
  )) {
    return;
  }

  try {

    await api.put(
      `/admin/companies/${id}/blacklist`
    );

    await searchCompanies();

  } catch (error) {

    alert(
      error?.response?.data?.message ||
      "Failed to blacklist company."
    );

  }

}


async function unblacklistCompany(id) {

  try {

    await api.put(
      `/admin/companies/${id}/unblacklist`
    );

    await searchCompanies();

  } catch (error) {

    alert(
      error?.response?.data?.message ||
      "Failed to remove blacklist."
    );

  }

}


onMounted(() => {

  searchCompanies();

});

</script>