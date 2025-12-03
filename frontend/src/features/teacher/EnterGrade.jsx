"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";


export default function EnterGradeForm() {
  const [form, setForm] = useState({
    student: "",
    subject: "",
    score: "",
    comments: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("/api/grades/enter/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access")}`,
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Failed to submit grade");
      }

      setMessage("Grade submitted successfully!");
      setForm({ student: "", subject: "", score: "", comments: "" });
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-10 text-center text-2xl font-bold tracking-tight text-white">
          Enter Grade
        </h2>
        <p className="text-center text-gray-400 mt-2">
          Teachers can submit grades for any student.
        </p>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-md bg-gray-900 p-6 rounded-xl shadow-xl border border-gray-700">
        <form onSubmit={handleSubmit} className="space-y-6">

          <div>
            <Label htmlFor="student" className="text-gray-300">Student ID</Label>
            <Input
              name="student"
              value={form.student}
              onChange={handleChange}
              placeholder="Enter student ID"
              required
              className="mt-2"
            />
          </div>

          <div>
            <Label htmlFor="subject" className="text-gray-300">Subject</Label>
            <Input
              name="subject"
              value={form.subject}
              onChange={handleChange}
              placeholder="e.g. Mathematics"
              required
              className="mt-2"
            />
          </div>

          <div>
            <Label htmlFor="score" className="text-gray-300">Score</Label>
            <Input
              type="number"
              name="score"
              value={form.score}
              onChange={handleChange}
              placeholder="0 - 100"
              required
              className="mt-2"
            />
          </div>

          <div>
            <Label htmlFor="comments" className="text-gray-300">Comments</Label>
            <Textarea
              name="comments"
              value={form.comments}
              onChange={handleChange}
              placeholder="Optional notes about performance"
              className="mt-2"
            />
          </div>

          <Button type="submit" disabled={loading} className="w-full text-white">
            {loading ? "Submitting..." : "Submit Grade"}
          </Button>

          {message && (
            <p className="text-center text-sm text-gray-300 mt-3">{message}</p>
          )}

        </form>
      </div>
    </div>
  );
}
