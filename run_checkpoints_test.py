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



import sys
class _InfoDebugFilter(logging.Filter):
    """Creates a filter for only logging records of INFO level or lower
    (ie records that should print in black)

    From url-imports/urlimports/util.py
    """

    def filter(self, record):
        """Defines the filter for records of INFO level or less"""
        return record.levelno <= 20  # INFO level


def configure_logging(list_of_modules=None, level=logging.INFO, frmt='%(message)s'):
    """Takes list of modules sets logging level to ERROR. Default = no modules.
    Takes level and sets root LOG level. Default = INFO
    Takes format string and sets format. Default = '%(message)s'.

    Configures two LOG handlers, one for WARNING and higher to stderr
    (and so printed in red on Platform) and one for INFO and lower to stdout
    (and so printed in black on Platform)
    """
    formatter = logging.Formatter(frmt)

    log = logging.getLogger()
    log.setLevel(level)

    red_handling = logging.StreamHandler(sys.stderr)
    red_handling.setLevel(logging.WARNING)
    red_handling.setFormatter(formatter)
    log.addHandler(red_handling)

    black_handling = logging.StreamHandler(sys.stdout)
    black_handling.setLevel(logging.DEBUG)
    black_handling.setFormatter(formatter)

    # Necessary because default behavior is to put in everything OVER the level in above line
    # But red_handling already does this for things over INFO and don't want duplicates
    black_handling.addFilter(_InfoDebugFilter())
    log.addHandler(black_handling)

    if list_of_modules:
        for module in list_of_modules:
            logging.getLogger(module).setLevel(logging.ERROR)


if __name__ == "__main__":
    configure_logging()
    
    import great_expectations as ge
    context = ge.data_context.DataContext()
    checkpoint = context.get_checkpoint("prod.chk")
    results = run_checkpoint(context, checkpoint)


