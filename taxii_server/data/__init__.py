from blinker import signal

from ..signals import POST_SAVE_CONTENT_BLOCK


class DataManager(object):

    def __init__(self, config, api):
        self.config = config
        self.api = api

        for _type, id, props in config.services:
            self.create_service(_type, props, id=id)

    # To be replaced
    def create_service(self, type, properties, id=None):
        self.api.save_service(id=id, type=type, properties=properties)

    def assign_collection(self, coll_id, services_ids):
        return self.api.assign_collection(coll_id, services_ids)
    ####

    def get_services(self):
        return self.api.get_services()

    def get_service_ids_for_collection(self, collection, service_type):
        services = self.api.get_services(collection_id=collection.id,
                service_type=service_type)

        return map(lambda (type, id, opts): id, services)

    def get_collections(self, service_id=None):
        return self.api.get_collections(service_id=service_id)

    def get_collection(self, name, service_id):
        return self.api.get_collection(name, service_id)

    def save_collection(self, entity):
        return self.api.save_collection(entity)

    def save_content(self, content, service_id=None, inbox_message=None,
            collections=[]):

        if inbox_message:
            inbox_message = self.api.save_inbox_message(inbox_message, service_id=service_id)
            content.inbox_message_id = inbox_message.id

        content = self.api.save_content(content)

        collection_ids = [c.id for c in collections]

        if collection_ids:
            self.api.add_content(content, collection_ids)

        signal(POST_SAVE_CONTENT_BLOCK).send(self, content_block=content,
                collection_ids=collection_ids)

        return content

    def get_content_count(self, collection_id, start_time=None, end_time=None,
            bindings=[]):

        return self.api.get_content_count(
            collection_id = collection_id,
            start_time = start_time,
            end_time = end_time,
            bindings = bindings,
        )

    def get_content(self, collection_id, count_only=False, start_time=None,
            end_time=None, bindings=[], offset=0, limit=10):

        return self.api.get_content(
            collection_id = collection_id,
            start_time = start_time,
            end_time = end_time,
            bindings = bindings,
            offset = offset,
            limit = limit,
        )


    def save_result_set(self, result_set_entity):
        return self.api.save_result_set(result_set_entity)

    def get_result_set(self, result_set_id):
        return self.api.get_result_set(result_set_id)

    def create_subscription(self, subscription):
        return self.api.save_subscription(subscription)

    def get_subscription(self, subscription_id):
        return self.api.get_subscription(subscription_id)

    def update_subscription(self, subscription, new_status):
        subscription.status = new_status
        return self.api.save_subscription(subscription)

