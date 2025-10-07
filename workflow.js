'use strict';

/**
 * Triggers a predefined n8n workflow with the provided input payload.
 *
 * @param {unknown} input - Arbitrary payload data to forward to n8n.
 * @returns {Promise<string>} A confirmation message once the workflow is triggered.
 */
async function main(input) {
  const { n8n } = tools;

  await n8n.workflow.trigger('N8N_WORKFLOW_ID', {
    payload: input,
  });

  return 'Workflow gestartet.';
}

module.exports = {
  main,
};
