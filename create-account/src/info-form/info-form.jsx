import React, { useState } from 'react';
import './info-form.css';

const InfoForm = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        username: '',
        password: '',
        major: '',
        classStanding: '',
        languages: '',
        desiredProject: '',
        desiredRole: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };

    return (
        <form class="signup-form" onSubmit={handleSubmit}>
            <div class="title">Create Your HackerMatch Profile</div>
            <div class="form-container">
                <div class="oneHalf">
                    <div class="form-group1">
                        <label>First Name:</label>
                        <input type="text" name="firstName" value={formData.firstName} onChange={handleChange} required />
                    </div>
                    <div class="form-group1">
                        <label>Last Name:</label>
                        <input type="text" name="lastName" value={formData.lastName} onChange={handleChange} required />
                    </div>
                    <div class="form-group1">
                        <label>Email:</label>
                        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                    </div>
                    <div class="form-group1">
                        <label>Username:</label>
                        <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                    </div>
                    <div class="form-group1">
                        <label>Password:</label>
                        <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                    </div>
                </div>
                <div class="twoHalf"> 
                    <div class="form-group2">
                        <label>College Major:</label>
                        <input type="text" name="major" value={formData.major} onChange={handleChange} required />
                    </div>
                    <div class="form-group2">
                        <label>Class Standing:</label>
                        <select name="classStanding" value={formData.classStanding} onChange={handleChange} required>
                            <option value="">Select...</option>
                            <option value="Freshman">Freshman</option>
                            <option value="Sophomore">Sophomore</option>
                            <option value="Junior">Junior</option>
                            <option value="Senior">Senior</option>
                            <option value="Grad Student">Grad Student</option>
                        </select>
                    </div>
                    <div class="form-group2">
                        <label>Skills (Programming Languages, Frameworks, etc.):</label>
                        <input type="text" name="skills" value={formData.skills} onChange={handleChange} required />
                    </div>
                    <div class="form-group2">
                        <label>Desired Project(s):</label>
                        <input type="text" name="desiredProject" value={formData.desiredProject} onChange={handleChange} />
                    </div>
                    <div class="form-group2">
                        <label>Desired Role:</label>
                        <input type="text" name="desiredRole" value={formData.desiredRole} onChange={handleChange} />
                    </div>
                </div>
            </div>
            <div class="button-container">
                <button type="submit">Submit</button>
            </div>
        </form>
    );
    
}
export default InfoForm;
