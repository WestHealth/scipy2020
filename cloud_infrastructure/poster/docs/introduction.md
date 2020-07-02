# Overview

## Why is security important?

   * Having a secure environment allows access to more sensitive and private data
   * Many data use agreements include security compliance
   * Health related data might be subject to HIPAA requirements
   * Data breaches are in general bad

## What is this poster about?

   * We built a secure cloud platform for data analysis
   * We feature Jupyter but extend the concept to other applications
   * We try to keep the principlel here simple
      - Security through simplicity
   * The system requires less effort to maintain by leveraging features provided the our cloud provider Amazon Web Services (AWS)

## Pitfalls of other approaches

   * Jupyter Hub does not have any well establish solutions for encryption, especially in transit
   * Kubernetes is not by default secure and requires significant effort to secure.
   * Kubernetes is very complex

## In a nutshell

   * Elastic Container Service is used
   * Leverage the Application Load Balancer for authentication through an external identity provider
   * Secure attached storage for collaboration
   * Underlying EC2 instances are secured through installation of a variety of agents
