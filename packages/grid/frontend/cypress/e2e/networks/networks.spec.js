// very rudimentary :)
describe('PyGrid Domain: viewing available and connected networks', () => {
  beforeEach(() => {
    // put stubs here
    cy.visit('http://localhost/networks')
  })

  it('should have the Network heading and description', () => {
    cy.findByRole('heading', {name: 'Networks'}).should('exist')
    // just a partial match
    cy.findByText(/Networks are the primary way you’ll attract Data Scientists to your Domain node/i).should('exist')
  })

  it('should be able to view details of the available network', () => {
    cy.findByText('Guest').should('exist')
    cy.findByRole('button', {name: 'Leave Network'}).should('exist')
    cy.findByText('United Nations').should('exist').click()
    cy.findAllByRole('region')
      .eq(0)
      .within($insideUN => {
        // tests are now focused inside the "United Nations" panel
        cy.findByText('ID#:').should('exist')
        cy.findByText('21a68e773ba747f0a4b6169bf28e8bed').should('exist')
        cy.findByRole('link', {name: 'https://un.openmined.org'}).should('have.length', 1)
        cy.findByText(/hosted domains/i).should('exist')
        cy.findByText(/hosted datasets/i).should('exist')
        cy.findByText(/all tags/i).should('exist')
        cy.findByText(/commodities/i).should('exist')
      })
  })

  it('should be possible to leave a network', () => {
    cy.findAllByRole('button', {name: 'Leave Network'}).should('have.length', 1)
    cy.findAllByRole('button', {name: 'Join as Guest'}).should('have.length', 1)
    cy.findAllByText('Not a member').should('have.length', 1)
    cy.findAllByText('Guest').should('have.length', 1)
    cy.findByRole('button', {name: 'Leave Network'}).click()
    cy.findAllByRole('button', {name: 'Join as Guest'}).should('have.length', 2)
    cy.findAllByText('Not a member').should('have.length', 2)
  })

  it('should be possible to join a network', () => {
    cy.findAllByRole('button', {name: 'Leave Network'}).should('have.length', 1)
    cy.findAllByRole('button', {name: 'Join as Guest'}).should('have.length', 1)
    cy.findAllByText('Not a member').should('have.length', 1)
    cy.findAllByText('Guest').should('have.length', 1)
    cy.findByRole('button', {name: 'Join as Guest'}).click()
    cy.findAllByRole('button', {name: 'Leave Network'}).should('have.length', 2)
    cy.findAllByText('Not a member').should('have.length', 2)
  })
})
