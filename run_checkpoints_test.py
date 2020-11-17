import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def run_checkpoint(context, checkpoint):
    # Get configuration and Expectation Suites for every batch in the current checkpoint.
    batches_to_validate = []
    for batch in checkpoint["batches"]:
        batch_kwargs = batch["batch_kwargs"]
        for suite_name in batch["expectation_suite_names"]:
            LOG.info("Getting batch for suite %s: %s", suite_name, batch_kwargs)
            suite = context.get_expectation_suite(suite_name)
            batch = context.get_batch(batch_kwargs, suite)
            LOG.info("Adding the following batch to the list to be executed: %s", batch)
            batches_to_validate.append(batch)
    # Run the validation operator on all batches found.
    LOG.info("Executing %s batches", len(batches_to_validate))
    results = context.run_validation_operator(
        checkpoint["validation_operator_name"],
        assets_to_validate=batches_to_validate,
    )
    return results


import great_expectations as ge
context = ge.data_context.DataContext()
checkpoint = context.get_checkpoint("prod.chk")
results = run_checkpoint(context, checkpoint)
