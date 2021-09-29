describe('PyGrid Domain: viewing available and connected networks', () => {
  beforeEach(() => {
    // put stubs here
    cy.visit('/')
  })

  it('should be able to visit the Networks section', () => {
    cy.get('nav')
      .findByText(/networks/i)
      .click()
      .url()
      .should('include', '/networks')
  })
})
