import React from 'react';
import axios from 'axios';
import { useState,useEffect } from 'react';

const AllJobs = () => {
    const [jobs, setJobs] = useState([]);

    const fetchJobs = async () => {
        const response = await axios.get('http://localhost:8000/api');
        setJobs(response.data);
    }

    useEffect(() => {
        fetchJobs();
    }, []);

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">All Jobs</h1>
            <div className="w-full max-w-2xl">
                {jobs.length > 0 ? (
                    jobs.map((job) => (
                        <div key={job.id} className="border p-4 mb-4 rounded shadow">
                            <h2 className="text-xl font-semibold">{job.name}</h2>
                            <p className="text-gray-700">{job.number}</p>
                            <p className="text-gray-500">Location: {job.marital_status}</p>
                            <p className="text-gray-500">Salary: {job.nationality}</p>
                            <img src={job.photo_upload} alt={job.name} className="w-32 h-32 object-cover mt-2" />
                        </div>
                    ))
                ) : (
                    <p className="text-lg">No jobs available at the moment.</p>
                )}
            </div>
        </div>
    );
};

export default AllJobs;