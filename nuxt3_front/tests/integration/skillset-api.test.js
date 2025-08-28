/**
 * Integration Test for SkillSetList Component API Behavior
 * 
 * This test verifies that:
 * 1. The API Gateway is accessible
 * 2. The corrections endpoint returns skills data
 * 3. The data structure matches what the component expects
 * 
 * Run with real services: docker-compose up
 */

import { describe, it, expect } from 'vitest'

const API_BASE_URL = 'http://localhost:8080'

describe('SkillSetList Integration', () => {
  it('should fetch skills from corrections API', async () => {
    const response = await fetch(`${API_BASE_URL}/corrections?correction_type=skill`)
    
    expect(response.ok).toBe(true)
    expect(response.status).toBe(200)
    
    const skills = await response.json()
    
    // Verify data structure
    expect(Array.isArray(skills)).toBe(true)
    expect(skills.length).toBeGreaterThan(0)
    
    // Check first skill has expected properties
    const firstSkill = skills[0]
    expect(firstSkill).toHaveProperty('id')
    expect(firstSkill).toHaveProperty('text')
    expect(firstSkill).toHaveProperty('type')
    expect(firstSkill.type).toBe('skill')
    
    // Verify UUID format for id
    expect(firstSkill.id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i)
    
    // Verify text content
    expect(typeof firstSkill.text).toBe('string')
    expect(firstSkill.text.length).toBeGreaterThan(0)
    
    console.log(`✅ Successfully fetched ${skills.length} skills`)
    console.log(`📋 Sample skill: ${firstSkill.text}`)
  })

  it('should fetch words from corrections API', async () => {
    const response = await fetch(`${API_BASE_URL}/corrections?correction_type=word`)
    
    expect(response.ok).toBe(true)
    const words = await response.json()
    
    expect(Array.isArray(words)).toBe(true)
    expect(words.length).toBeGreaterThan(0)
    expect(words[0].type).toBe('word')
    
    console.log(`✅ Successfully fetched ${words.length} words`)
  })

  it('should fetch sentences from corrections API', async () => {
    const response = await fetch(`${API_BASE_URL}/corrections?correction_type=sentence`)
    
    expect(response.ok).toBe(true)
    const sentences = await response.json()
    
    expect(Array.isArray(sentences)).toBe(true)
    expect(sentences.length).toBeGreaterThan(0)
    expect(sentences[0].type).toBe('sentence')
    
    console.log(`✅ Successfully fetched ${sentences.length} sentences`)
  })

  it('should fetch jobtypes for dropdown', async () => {
    const response = await fetch(`${API_BASE_URL}/files/jobtypes`)
    
    expect(response.ok).toBe(true)
    const result = await response.json()
    
    expect(result).toHaveProperty('data')
    expect(Array.isArray(result.data)).toBe(true)
    expect(result.data.length).toBeGreaterThan(0)
    
    const firstJobtype = result.data[0]
    expect(firstJobtype).toHaveProperty('id')
    expect(firstJobtype).toHaveProperty('name')
    expect(firstJobtype).toHaveProperty('category')
    
    console.log(`✅ Successfully fetched ${result.data.length} jobtypes`)
  })

  it('should fetch industries for dropdown', async () => {
    const response = await fetch(`${API_BASE_URL}/files/industries`)
    
    expect(response.ok).toBe(true)
    const result = await response.json()
    
    expect(result).toHaveProperty('data')
    expect(Array.isArray(result.data)).toBe(true)
    expect(result.data.length).toBeGreaterThan(0)
    
    const firstIndustry = result.data[0]
    expect(firstIndustry).toHaveProperty('id')
    expect(firstIndustry).toHaveProperty('name')
    expect(firstIndustry).toHaveProperty('sector')
    
    console.log(`✅ Successfully fetched ${result.data.length} industries`)
  })
})