# -*- coding: utf-8 -*-

"""Contain util function to help the code work better."""


class Log(object):

    """
        Classe responsável por implementar métodos auxiliares para o uso de LOGs.
    """

    @classmethod
    def add_header(cls, logr, file_name, obj_instance, class_obj=None):
        class_name = "Class name Undefined"
        if obj_instance:
            class_name = obj_instance.__class__.__name__
        elif class_obj:
            class_name = class_obj.__name__

        logr.debug('########## ' +
                   '.'.join(
                       [str(file_name), str(class_name)]) +
                   ': ##########')

    @classmethod
    def add_footer(cls, logr):
        logr.debug('---------------------\n')

    @classmethod
    def add_user(cls, logr, user_name):
        logr.debug('USER: {user}'.format(user=user_name))

    @classmethod
    def add_exception(cls, logr, exception_message):
        logr.debug('EXCEPTION: {exception_message}'.
                   format(exception_message=exception_message))

    @classmethod
    def item_yield(cls, logr, item_obj):
        logr.debug('{class_name} yielded: {obj_atrrs}'.
                   format(class_name=item_obj.__class__.__name__,
                          obj_atrrs=str(item_obj)))

    @classmethod
    def model_commited_on_db(cls, logr, item_obj):
        logr.debug('{class_name} commited on DB: {obj_atrrs}'.
                   format(class_name=item_obj.__class__.__name__,
                          obj_atrrs=str(item_obj)))
