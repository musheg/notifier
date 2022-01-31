import yaml


class Notifier:
    def __init__(self, entity_obj, original_entity_obj, entity_type):
        # TODO: hanle invalid configs error
        with open("configs.yaml", "r") as configs:
            configs = yaml.safe_load(configs)
        self.configs = configs[entity_type]
        self.obj = entity_obj
        self.obj_before_update = original_entity_obj

    def __should_be_notified(self):
        # new entity has been added
        if self.configs.get('is_new'):
            if self.obj_before_update is None:
                return True

        # the entity physically deleted
        if self.configs.get('is_deleted'):
            if self.obj is None:
                return True

        # attributes of entity changed
        if self.configs.get('changed_attrs'):
            for changed_attr in self.configs.get('changed_attrs'):
                if getattr(self.obj, changed_attr) != getattr(self.obj_before_update, changed_attr):
                    return True

        # attributes of entity changed and currently have some specific states
        if self.configs.get('changed_attrs_with_current_value'):
            for changed_attr in self.configs.get('changed_attrs_with_current_value'):
                if all([
                    getattr(self.obj, changed_attr) != getattr(self.obj_before_update, changed_attr),
                    getattr(self.obj, changed_attr) in self.configs['changed_attrs_with_current_value'].get(changed_attr)
                ]):
                    return True
        return False

    def __get_alertable_entity(self):
        if self.configs.get('notify_on') == 'self':
            return self.obj
        else:
            # TODO: create custom exception raise and catch in case if we have invalid notify_on value
            return getattr(self.obj, self.configs['notify_on'])

    def notify(self):
        if self.__should_be_notified():
            print(f"send alert...")
            print(self.__get_alertable_entity())
        else:
            print('no need for alert.')
