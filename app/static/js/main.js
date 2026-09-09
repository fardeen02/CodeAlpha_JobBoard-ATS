//================================
//Logout time function
//================================

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

     if (sessionExpired) {
        alert("Your session has expired. Please log in again.");
    }

    window.location.href = "/login";
}

async function authFetch(url, options = {}) {

    const token = localStorage.getItem("token");

    if (!token) {
        logout();
        return;
    }

    const response = await fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        logout(true);
        throw new Error("Session expired");
    }

    return response;
} 

// ================================
// Navbar Scroll Effect
// ================================

const navbar = document.querySelector(".glass-nav");

if (navbar) {
    window.addEventListener("scroll", () => {
        navbar.style.background =
            window.scrollY > 40
                ? "rgba(9,9,22,.92)"
                : "rgba(9,9,22,.75)";
    });
}

//=================================
// Navbar - After Login (Button Change)
//=================================

const authButtons = document.getElementById("authButtons");

if (authButtons) {

    const token = localStorage.getItem("token");
    const user = JSON.parse(localStorage.getItem("user") || "null");

    if (token && user) {

        authButtons.innerHTML = `
            <span class="text-light me-3">
                Hello, ${user.name}
            </span>

            <button id="logoutBtn" class="btn btn-outline-light">
                Logout
            </button>
        `;

        document.getElementById("logoutBtn").addEventListener("click", () => {

            localStorage.removeItem("token");
            localStorage.removeItem("user");

            location.href = "/login";

        });

    }

}

// ================================
// Login
// ================================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    const message = document.getElementById("loginMessage");

    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword) {

        togglePassword.onclick = () => {

            const input = document.getElementById("password");

            input.type =
                input.type === "password"
                    ? "text"
                    : "password";

        };

    }

    loginForm.addEventListener("submit", async e => {

        e.preventDefault();

        const button = loginForm.querySelector("button[type='submit']");

        button.disabled = true;
        button.textContent = "Logging in...";

        try {

            const response = await fetch("/api/auth/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    email: document.getElementById("email").value,
                    password: document.getElementById("password").value

                })

            });

            const data = await response.json();

            if (response.ok) {

                localStorage.setItem("token", data.access_token);
                localStorage.setItem("user", JSON.stringify(data.user));

                message.className = "text-success mt-3";
                message.textContent = "Login successful!";

                setTimeout(() => {

                    if (data.user.role === "recruiter") {
                        location.href = "/recruiter";
                    } else {
                        location.href = "/jobs";
                    }

                }, 800);

            } else {

                message.className = "text-danger mt-3";
                message.textContent = data.error || "Login failed";

            }

        } catch {

            message.className = "text-danger mt-3";
            message.textContent = "Unable to connect to server.";

        }

        button.disabled = false;
        button.textContent = "Login";

    });

}

// ================================
// Register
// ================================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    const message = document.getElementById("registerMessage");

    const roleSelect = document.getElementById("role");
    const jobFields = document.getElementById("jobSeekerFields");

    // Show/Hide Job Seeker fields
    if (roleSelect && jobFields) {

        const toggleFields = () => {

            jobFields.style.display =
                roleSelect.value === "jobseeker"
                    ? "block"
                    : "none";

        };

        toggleFields();

        roleSelect.addEventListener("change", toggleFields);

    }

    registerForm.addEventListener("submit", async e => {

        e.preventDefault();

        const button = registerForm.querySelector("button[type='submit']");

        button.disabled = true;
        button.textContent = "Creating...";

        try {

            const response = await fetch("/api/auth/register", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    name: document.getElementById("name").value,
                    email: document.getElementById("regEmail").value,
                    password: document.getElementById("regPassword").value,
                    role: document.getElementById("role").value,
                    skills: document.getElementById("skills")?.value || "",
                    experience: Number(
                        document.getElementById("experience")?.value || 0
                    )

                })

            });

            const data = await response.json();

            if (response.ok) {

                message.className = "text-success mt-3";
                message.textContent = "Account created successfully!";

                setTimeout(() => {

                    location.href = "/login";

                }, 1200);

            } else {

                message.className = "text-danger mt-3";
                message.textContent =
                    data.error || "Registration failed";

            }

        } catch {

            message.className = "text-danger mt-3";
            message.textContent = "Unable to connect to server.";

        }

        button.disabled = false;
        button.textContent = "Create Account";

    });

}

// ================================
// Jobs Page
// ================================

const jobsContainer=document.getElementById("jobsContainer");

if(jobsContainer){

    let jobs=[];

    async function loadJobs(){

        jobsContainer.innerHTML="<p class='text-secondary'>Loading jobs...</p>";

        const response=await fetch("/api/jobs");
        const data=await response.json();

        jobs=data.jobs;

        renderJobs(jobs);

    }

    function renderJobs(list){

        if(list.length===0){

            jobsContainer.innerHTML="<h4 class='text-secondary text-center'>No jobs found.</h4>";
            return;

        }

        jobsContainer.innerHTML=list.map(job=>`

        <div class="col-md-6 col-lg-4">

            <div class="job-card h-100">

                <div class="company-icon">${job.company[0]}</div>

                <h4>${job.title}</h4>

                <p class="company-name">${job.company}</p>

                <div class="job-meta">

                    <span>📍 ${job.location}</span>

                    <span>${job.salary ? "₹"+job.salary : "Negotiable"}</span>

                </div>

                <p class="mt-3">${job.employment_type}</p>

                <a href="/jobs/${job.job_id}" class="btn btn-primary w-100 mt-3">
                    View Details
                </a>

            </div>

        </div>

        `).join("");

    }

    document.getElementById("searchInput").addEventListener("input",e=>{

        const value=e.target.value.toLowerCase();

        renderJobs(

            jobs.filter(job=>

                job.title.toLowerCase().includes(value) ||
                job.company.toLowerCase().includes(value) ||
                job.location.toLowerCase().includes(value)

            )

        );

    });

    loadJobs();

}

// ================================
// Job Details Page
// ================================


const jobDetails = document.getElementById("jobDetails");

if (jobDetails && typeof JOB_ID !== "undefined") {
    loadJob();
}

async function loadJob() {

    const response = await fetch("/api/jobs");
    const data = await response.json();

    const job = data.jobs.find(j => j.job_id === JOB_ID);

    if (!job) {
        jobDetails.innerHTML = "<h3 class='text-center'>Job Not Found</h3>";
        return;
    }

    jobDetails.innerHTML = `
    <div class="col-lg-8">
        <div class="job-card">

            <h1>${job.title}</h1>

            <p class="company-name fs-5">${job.company}</p>

            <div class="job-meta mt-3">
                <span>📍 ${job.location}</span>
                <span>${job.salary ? "₹"+job.salary : "Negotiable"}</span>
            </div>

            <hr>
            <h4>Skills</h4>
            <p>${job.skills_required || "No skills needed."}</p>
			
            <h4>Description</h4>
            <p>${job.description || "No description available."}</p>

            <h4 class="mt-4">Employment</h4>
            <p>${job.employment_type}</p>

        </div>
    </div>

    <div class="col-lg-4">

        <div class="job-card position-sticky" style="top:6rem;">

            <h4>Quick Apply</h4>

            <p class="text-secondary">
                Upload your resume and receive an ATS match score.
            </p>

            <form id="resumeForm">

                <input
                    type="file"
                    id="resumeFile"
                    class="form-control mb-3"
                    accept=".pdf"
                    required
                >

                <button
                    id="applyBtn"
                    class="btn btn-primary w-100"
                    type="submit"
                >
                    Apply Now
                </button>

            </form>

            <div id="applyMessage" class="mt-3 text-center"></div>

            <div id="atsResult" class="mt-4" style="display:none;">

                <div class="stat-card">

                    <h3 id="matchScore">0%</h3>

                    <p>ATS Match Score</p>

                    <div id="foundSkills" class="skills mt-3"></div>

                </div>

            </div>

        </div>

    </div>
    `;

    const resumeForm = document.getElementById("resumeForm");

    resumeForm.addEventListener("submit", async e => {

        e.preventDefault();

        const token = localStorage.getItem("token");

        if (!token) {
            location.href = "/login";
            return;
        }

        const file = document.getElementById("resumeFile").files[0];

        if (!file) return;

        const applyBtn = document.getElementById("applyBtn");
        const message = document.getElementById("applyMessage");

        applyBtn.disabled = true;
        applyBtn.textContent = "Applying...";

        try {

            const applyRes = await fetch(`/api/jobs/${JOB_ID}/apply`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            const applyData = await applyRes.json();

            if (!applyRes.ok) {

                message.className = "text-danger";
                message.textContent = applyData.error || "Application failed.";

                applyBtn.disabled = false;
                applyBtn.textContent = "Apply Now";

                return;
            }

            const formData = new FormData();
            formData.append("resume", file);

            const uploadRes = await fetch(
                `/api/jobs/applications/${applyData.application.app_id}/resume`,
                {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    },
                    body: formData
                }
            );

            const uploadData = await uploadRes.json();

            if (uploadRes.ok) {

                message.className = "text-success";
                message.textContent = "Resume uploaded successfully!";

                document.getElementById("atsResult").style.display = "block";
                document.getElementById("matchScore").textContent = `${uploadData.match_score}%`;

                document.getElementById("foundSkills").innerHTML =
                    uploadData.resume_skills
                        .map(skill => `<span>${skill}</span>`)
                        .join("");

                applyBtn.textContent = "Applied";

            } else {

                message.className = "text-danger";
                message.textContent = uploadData.error;

                applyBtn.disabled = false;
                applyBtn.textContent = "Apply Now";

            }

        } catch {

            message.className = "text-danger";
            message.textContent = "Server error.";

            applyBtn.disabled = false;
            applyBtn.textContent = "Apply Now";

        }

    });

}

// ================================
// Recruiter Dashboard
// ================================

// ================================
// Recruiter Dashboard
// ================================

const recruiterJobs = document.getElementById("recruiterJobs");

if (recruiterJobs) {
    loadRecruiterDashboard();
}

async function loadRecruiterDashboard() {

    try {

        const response = await authFetch("/api/recruiter/applicants");

        if (!response) return;

        const data = await response.json();

        if (!response.ok) {

            recruiterJobs.innerHTML =
                "<h3 class='text-center text-danger'>Unable to load dashboard.</h3>";

            return;
        }

        let totalJobs = data.jobs.length;
        let totalApplicants = 0;
        let totalScore = 0;

        data.jobs.forEach(job => {

            totalApplicants += job.total_applicants;

            job.applicants.forEach(app => {

                totalScore += app.match_score || 0;

            });

        });

        const avg = totalApplicants
            ? Math.round(totalScore / totalApplicants)
            : 0;

        document.getElementById("totalJobs").textContent = totalJobs;
        document.getElementById("totalApplicants").textContent = totalApplicants;
        document.getElementById("avgScore").textContent = `${avg}%`;

        recruiterJobs.innerHTML = data.jobs.map(job => `

            <div class="job-card mb-4">

                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">

                    <div>
                        <h3>${job.title}</h3>

                        <p class="company-name">
                            ${job.company || ""}
                        </p>
                    </div>

                    <span class="badge bg-primary rounded-pill px-3 py-2">
                        ${job.total_applicants} Applicants
                    </span>

                </div>

                <hr>

                ${
                    job.applicants.length === 0

                    ? `
                        <p class="text-secondary">
                            No applicants yet.
                        </p>
                    `

                    : job.applicants.map(app => {

                        const status =
                            (app.status || "pending").toLowerCase();

                        const isPending = status === "pending";

                        return `

                            <div class="applicant-card">

                                <div>

                                    <strong>
                                        ${app.name}
                                    </strong>

                                    <div class="small text-secondary">
                                        ${app.email}
                                    </div>

                                    <div class="small text-secondary mt-1">
                                        ${app.resume_skills || "No skills"}
                                    </div>

                                </div>

                                <div class="text-end">

                                    <span class="score-badge ${
                                        app.match_score >= 80
                                            ? "score-green"
                                            : app.match_score >= 50
                                                ? "score-yellow"
                                                : "score-red"
                                    }">

                                        ${app.match_score || 0}%

                                    </span>

                                    <div class="small mt-2 text-capitalize">
                                        Status: ${status}
                                    </div>

                                    ${
                                        isPending
                                            ? `
                                                <div class="d-flex gap-2 mt-3 justify-content-end">

                                                    <button
                                                        class="btn btn-success btn-sm status-btn"
                                                        data-app-id="${app.app_id}"
                                                        data-status="accepted">
                                                        Accept
                                                    </button>

                                                    <button
                                                        class="btn btn-danger btn-sm status-btn"
                                                        data-app-id="${app.app_id}"
                                                        data-status="rejected">
                                                        Reject
                                                    </button>

                                                </div>
                                            `
                                            : ""
                                    }

                                </div>

                            </div>

                        `;

                    }).join("")
                }

            </div>

        `).join("");

        // ================================
        // Accept / Reject Button Events
        // ================================

        recruiterJobs
            .querySelectorAll(".status-btn")
            .forEach(button => {

                button.addEventListener("click", async () => {

                    const appId =
                        Number(button.dataset.appId);

                    const status =
                        button.dataset.status;

                    await updateApplicationStatus(
                        appId,
                        status
                    );

                });

            });

    } catch (error) {

        if (error.message === "Session expired") {
            return;
        }

        console.error(
            "Recruiter dashboard error:",
            error
        );

        recruiterJobs.innerHTML =
            "<h3 class='text-center text-danger'>Unable to load dashboard.</h3>";
    }
}


// ================================
// Accept / Reject Application
// ================================

async function updateApplicationStatus(appId, status) {

    const action =
        status === "accepted"
            ? "accept"
            : "reject";

    const confirmed = confirm(
        `Are you sure you want to ${action} this applicant?`
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await authFetch(
            `/api/recruiter/applications/${appId}/status`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: status
                })
            }
        );

        if (!response) return;

        const data = await response.json();

        if (!response.ok) {

            alert(
                data.error ||
                "Unable to update application status."
            );

            return;
        }

        alert(
            status === "accepted"
                ? "Applicant accepted successfully!"
                : "Applicant rejected successfully!"
        );

        // Reload dashboard so status changes immediately
        await loadRecruiterDashboard();

    } catch (error) {

        if (error.message === "Session expired") {
            return;
        }

        console.error(
            "Status update error:",
            error
        );

        alert(
            "Unable to update application status."
        );
    }
}

// ================================
// Create Job
// ================================

const createJobForm=document.getElementById("createJobForm");

if(createJobForm){

    const message=document.getElementById("createJobMessage");

    createJobForm.addEventListener("submit",async e=>{

        e.preventDefault();

        const token=localStorage.getItem("token");

        if(!token){

            location.href="/login";
            return;

        }

        const button=createJobForm.querySelector("button");

        button.disabled=true;
        button.textContent="Publishing...";

        try{

            const response=await fetch("/api/jobs",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json",
                    "Authorization":`Bearer ${token}`
                },

                body:JSON.stringify({

                    title:document.getElementById("jobTitle").value,
                    company:document.getElementById("company").value,
                    location:document.getElementById("location").value,
                    salary:Number(document.getElementById("salary").value)||null,
                    employment_type:document.getElementById("employmentType").value,
                    skills_required:document.getElementById("skillsRequired").value,
                    description:document.getElementById("description").value

                })

            });

            const data=await response.json();

            if(response.ok){

                message.className="text-success mt-3";
                message.textContent="Job published successfully!";

                setTimeout(()=>{

                    location.href="/recruiter";

                },1000);

            }else{

                message.className="text-danger mt-3";
                message.textContent=data.error||"Unable to publish.";

            }

        }catch{

            message.className="text-danger mt-3";
            message.textContent="Server connection failed.";

        }

        button.disabled=false;
        button.textContent="Publish Job";

    });

}

//================================================
// Dynamic stats Home Page
//================================================

const counters=document.querySelectorAll(".counter");

if(counters.length){

    loadStats();

}

async function loadStats(){

    const response=await fetch("/api/stats");

    const stats=await response.json();

    const values=[
        stats.jobs,
        stats.recruiters,
        stats.applicants,
        stats.accuracy
    ];

    counters.forEach((counter,index)=>{

        animateCounter(counter,values[index]);

    });

}

function animateCounter(counter,target){

    let current=0;

    const increment=Math.max(1,Math.ceil(target/50));

    const timer=setInterval(()=>{

        current+=increment;

        if(current>=target){

            current=target;

            clearInterval(timer);

        }

        counter.textContent=current;

    },20);

}

//==============================================
//Feature Loading Job - Dynamically in Home Page
//==============================================

async function loadFeaturedJobs() {

    const container = document.getElementById("featuredJobs");

    if (!container) return;

    try {

        const response = await fetch("/api/jobs");

        if (!response.ok) {
            throw new Error("Failed to load jobs");
        }

        const data = await response.json();

        const jobs = data.jobs || [];

        if (jobs.length === 0) {

            container.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-secondary">
                        No job opportunities available right now.
                    </p>
                </div>
            `;

            return;
        }

        const featuredJobs = jobs.slice(0, 3);

        container.innerHTML = featuredJobs.map(job => {

            const skills = job.skills_required
                ? job.skills_required
                    .split(",")
                    .map(skill => skill.trim())
                    .filter(skill => skill)
                    .slice(0, 3)
                : [];

            const skillsHTML = skills.length
                ? skills.map(skill => `<span>${skill}</span>`).join("")
                : `<span>${job.employment_type || "Full-time"}</span>`;

            return `
                <div class="col-md-6 col-lg-4">

                    <div class="job-card">

                        <div class="company-icon">
                            ${job.company
                                ? job.company.charAt(0).toUpperCase()
                                : "N"}
                        </div>

                        <h4>${job.title}</h4>

                        <p class="company-name">
                            ${job.company}
                        </p>

                        <div class="job-meta">

                            <span>
                                📍 ${job.location || "Not specified"}
                            </span>

                            <span>
                                ${job.salary
                                    ? "₹" + job.salary
                                    : "Negotiable"}
                            </span>

                        </div>

                        <div class="skills mt-3">
                            ${skillsHTML}
                        </div>

                        <a href="/jobs/${job.job_id}"
                           class="btn btn-primary w-100 mt-4">
                            View Job
                        </a>

                    </div>

                </div>
            `;
        }).join("");

    } catch (error) {

        console.error("Error loading featured jobs:", error);

        container.innerHTML = `
            <div class="col-12 text-center">
                <p class="text-secondary">
                    Unable to load job opportunities.
                </p>
            </div>
        `;
    }
}

if (document.getElementById("featuredJobs")) {
    loadFeaturedJobs();
}